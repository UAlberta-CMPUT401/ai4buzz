"""
Module containing class to create image collage
"""

"""
Source_code: https://github.com/twilsonco/PyPhotoCollage 

The MIT License (MIT)

Copyright (c) 2014 Dmitry Alimov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import random
import math
from PIL.ExifTags import TAGS
from PIL import ImageOps
from PIL import Image
from operator import itemgetter

class CollageGenerator:
    def __init__(self):
        pass

    def linear_partition(self, seq, k, dataList = None):
        if k <= 0:
            return []
        n = len(seq) - 1
        if k > n:
            return map(lambda x: [x], seq)
        table, solution = self.linear_partition_table(seq, k)
        k, ans = k-2, []
        if dataList == None or len(dataList) != len(seq):
            while k >= 0:
                ans = [[seq[i] for i in range(solution[n-1][k]+1, n+1)]] + ans
                n, k = solution[n-1][k], k-1
            ans = [[seq[i] for i in range(0, n+1)]] + ans
        else:
            while k >= 0:
                ans = [[dataList[i] for i in range(solution[n-1][k]+1, n+1)]] + ans
                n, k = solution[n-1][k], k-1
            ans = [[dataList[i] for i in range(0, n+1)]] + ans
        return ans

    def linear_partition_table(self, seq, k):
        n = len(seq)
        table = [[0] * k for x in range(n)]
        solution = [[0] * (k-1) for x in range(n-1)]
        for i in range(n):
            table[i][0] = seq[i] + (table[i-1][0] if i else 0)
        for j in range(k):
            table[0][j] = seq[0]
        for i in range(1, n):
            for j in range(1, k):
                table[i][j], solution[i-1][j-1] = min(
                    ((max(table[x][j-1], table[i][0]-table[x][0]), x) for x in range(i)),
                    key=itemgetter(0))
        return (table, solution)

    def clamp(self, v,l,h):
        return l if v < l else h if v > h else v

    def makeCollage(self, imgList, spacing, antialias, background, aspectratiofactor):
        # first upscale all images according to the maximum height of any image (downscaling would result in a terrible quality image if a very short image was included in the batch)
        maxHeight = max([img.height for img in imgList])
        if antialias:
            imgList = [img.resize((int(img.width / img.height * maxHeight),maxHeight), Image.ANTIALIAS) if img.height < maxHeight else img for img in imgList]
        else:
            imgList = [img.resize((int(img.width / img.height * maxHeight),maxHeight)) if img.height < maxHeight else img for img in imgList]
        
        # generate the input for the partition problem algorithm
        # need list of aspect ratios and number of rows (partitions)
        totalWidth = sum([img.width for img in imgList])
        avgWidth = totalWidth / len(imgList)
        targetWidth = avgWidth * math.sqrt(len(imgList) * aspectratiofactor)
        
        numRows = self.clamp(int(round(totalWidth / targetWidth)), 1, len(imgList))
        if numRows == 1:
            imgRows = [imgList]
        elif numRows == len(imgList):
            imgRows = [[img] for img in imgList]
        else:
            aspectRatios = [int(img.width / img.height * 100) for img in imgList]
        
            # get nested list of images (each sublist is a row in the collage)
            imgRows = self.linear_partition(aspectRatios, numRows, imgList)
        
            # scale down larger rows to match the minimum row width
            rowWidths = [sum([img.width + spacing for img in row]) - spacing for row in imgRows]
            minRowWidth = min(rowWidths)
            rowWidthRatios = [minRowWidth / w for w in rowWidths]
            if antialias:
                imgRows = [[img.resize((int(img.width * widthRatio), int(img.height * widthRatio)), Image.ANTIALIAS) for img in row] for row,widthRatio in zip(imgRows, rowWidthRatios)]
            else:
                imgRows = [[img.resize((int(img.width * widthRatio), int(img.height * widthRatio))) for img in row] for row,widthRatio in zip(imgRows, rowWidthRatios)]
        
        # populate new image
        rowWidths = [sum([img.width + spacing for img in row]) - spacing for row in imgRows]
        rowHeights = [max([img.height for img in row]) for row in imgRows]
        minRowWidth = min(rowWidths)
        w,h = (minRowWidth, sum(rowHeights) + spacing * (numRows - 1))
        
        if background == (0,0,0):
            background += tuple([0])
        else:
            background += tuple([255])
        outImg = Image.new("RGBA", (w,h), background)
        xPos,yPos = (0,0)
        
        for row in imgRows:
            for img in row:
                outImg.paste(img, (xPos,yPos))
                xPos += img.width + spacing
                continue
            yPos += max([img.height for img in row]) + spacing
            xPos = 0
            continue
        
        return outImg

    def generate(self, images):
        """ 
        generates a collage as an image object

        :images type: List of images
        :returns type: Collage
        """
        output_path = 'api/image_features/collage_generator/collage.png'
        width = 5000
        height = 5000
        initheight = 500
        shuffle = False
        imagegap = 5
        background = (25,25,25)
        aspectratiofactor = 1.0
        antialias = True     
        
        # shuffle images if needed
        if shuffle:
            random.shuffle(images)
        
        # Process PIL image objects for all the photos
        pilImages = []
        for img in images:
            # Need to explicitly tell PIL to rotate image if EXIF orientation data is present
            exif = img.getexif()
            # Remove all exif tags
            for k in exif.keys():
                if k != 0x0112:
                    exif[k] = None # If I don't set it to None first (or print it) the del fails for some reason. 
                    del exif[k]
            # Put the new exif object in the original image
            new_exif = exif.tobytes()
            img.info["exif"] = new_exif
            # Rotate the image
            img = ImageOps.exif_transpose(img)
            if initheight > 2 and img.height > initheight:
                if antialias:
                    pilImages.append(img.resize((int(img.width / img.height * initheight),initheight), Image.ANTIALIAS))
                else:
                    pilImages.append(img.resize((int(img.width / img.height * initheight),initheight)))
            else:
                pilImages.append(img)
        
        # takes list of PIL image objects and returns the collage as a PIL image object
        collage = self.makeCollage(pilImages, imagegap, antialias, background, aspectratiofactor)
        
        if width > 0 and collage.width > width:
            collage = collage.resize((width, int(collage.height / collage.width * width)), Image.ANTIALIAS)
            pass
        elif height > 0 and collage.height > height:
            collage = collage.resize((int(collage.width / collage.height * height), height), Image.ANTIALIAS)
            pass
        
        collage.save(output_path)
        return collage