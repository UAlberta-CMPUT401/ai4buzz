"""Contains class to recognize text in images."""

import cv2
import pytesseract
import numpy as np


class TextRecognizer:
    """Uses OpenCV to detect and tesseract to recognize text."""

    def __init__(self):
        try:
            pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
        except:
            pass

        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
        except:
            pass
    
    def get_descriptions(self, image) -> str:
        """image: PIL.JpegImagePlugin.JpegImageFile
        returns: Descreptions(descreptions=[('person', 0.99), ('boat', 0.77), ...])"""
        np_image = self._preprocess_image(image)
        contours = self._detect_text_and_return_bounding_boxes(np_image)
        text = self._recognize_text_from_detetions(np_image, contours)
        return text

    def _preprocess_image(self, image) -> np.ndarray:
        np_image = np.array(image)
        # Convert the image to gray scale
        grayscale_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
        
        # Performing OTSU threshold
        threshold_value, threshloded_image = cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        return threshloded_image

    def _detect_text_and_return_bounding_boxes(self, threshloded_image:  np.ndarray) ->  np.ndarray:
        # Specify structure shape (rectangle) and kernel size.
        # Kernel size increases or decreases the area of the rectangle to be detected.
        # A smaller value like (10, 10) will detect each word instead of a sentence.
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
        
        # Applying dilation on the threshold image
        dilation = cv2.dilate(threshloded_image, rect_kernel, iterations = 1)
        
        # Finding contours: a Python list of all the contours in the image.
        # Each individual contour is a Numpy array of
        # (x,y) coordinates of boundary points of the object.
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_NONE)
        return contours

    def _recognize_text_from_detetions(self, np_image: np.ndarray, contours) -> str:
        detected_text = []
        # Looping through the identified contours
        # Then rectangular part is cropped and passed on to pytesseract for extracting text from it
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # Cropping the text block for giving input to OCR
            cropped = np_image[y:y + h, x:x + w]
            
            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped)
            if self._is_valid_text_string(text):
                detected_text.append(text)
        return " ".join(detected_text)

    def _is_valid_text_string(self, text: str) -> bool:
        for ch in text:
            if str.isalnum(ch):
                return True
        return False
