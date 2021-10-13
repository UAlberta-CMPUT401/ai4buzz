import colorgram
import cv2 as cv
from skimage import io
import numpy as np

def getPalette(img, num_colours):
    colours = colorgram.extract(img,num_colours)
    return colours


def getPaletteKMeans(img,num_colours):
    image=io.imread(img)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    Z = image.reshape((-1,3))
    # convert to np.float32
    Z = np.float32(Z)
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = num_colours
    #centers = np.zeros(3)
    ret,label,center=cv.kmeans(Z,K,None,criteria,10,cv.KMEANS_RANDOM_CENTERS)
    # Now convert back into uint8, and make original image
    #print(center)
    centers = np.copy(center)
    center = np.uint8(center)

    return center
    

if __name__ == "__main__":
    test_colours = [[255,201,13], [237,27,36], [0,163,232]]
    print(getPalette('colour_test.jpg',3))

    print(getPaletteKMeans('colour_test.jpg',3))
    print(test_colours)
