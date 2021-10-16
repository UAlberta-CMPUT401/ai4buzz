import colorgram
import cv2 as cv
from skimage import io
from PIL import Image
import numpy as np

from api.models.feature_analyzer import FeatureAnalyzer


class ColorSchemeAnalyzer(FeatureAnalyzer):
    def get_descriptions(self, image):
        colour_palette = self._get_palette(image, 3)
        # k_means_colour_palette = self._get_palette_k_means(image, 3)
        return self._format_description(colour_palette)

    def _format_description(self, description):
        return {
            "count": len(description),
            "colors": [color.rgb for color in description]
        }

    def _get_palette(self, img, num_colours):
        colours = colorgram.extract(img,num_colours)
        return colours

    def _get_palette_k_means(self, img, num_colours):
        image = np.array(img)
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
    colorSchemeAnalyzer = ColorSchemeAnalyzer()
    test_colours = [[255,201,13], [237,27,36], [0,163,232]]
    print(colorSchemeAnalyzer._get_palette('colour_test.jpg',3))

    print(colorSchemeAnalyzer._get_palette_k_means('colour_test.jpg',3))
    print(test_colours)
