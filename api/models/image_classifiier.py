"""Contains class to classify images."""
import tensorflow as tf
import tensorflow_hub as hub

import requests
import PIL
from PIL import Image
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np

from typing import List
import descriptions
import image_classification_models


class ImageClassifier:
    """Uses pretrained models to classify images."""

    _model_name: str    

    def __init__(self, model_name: str = 'inception_v3') -> None:
        self._model_name = model_name    
    
    def get_descriptions(self, jpg_image):
        """image: PIL.JpegImagePlugin.JpegImageFile"""
        image = self._convert_image_to_array(jpg_image)
        image = self._process_image_for_model(image)
        predictions = self._make_prediction(image)
        return descriptions.Descriptions(feature="Image Classification", 
            model_name=self._model_name, descriptions=predictions)

    def _process_image_for_model(self, image, 
    image_size=256, dynamic_size=False, max_dynamic_size=512):
        """image: PIL.JpegImagePlugin.JpegImageFile"""
        """Returns: tf.python.framework.ops.EagerTensor"""
        if self._model_name in image_classification_models.model_image_size_map:
            # Images will be converted to {image_size}x{image_size}
            image_size = image_classification_models.model_image_size_map[self._model_name]
            dynamic_size = False
        else:
            # Images will be capped to a max size of {max_dynamic_size}x{max_dynamic_size}
            dynamic_size = True

        if tf.reduce_max(image) > 1.0:
            image = image / 255.
        if len(image.shape) == 3:
            image = tf.stack([image, image, image], axis=-1)
        if not dynamic_size:
            image = tf.image.resize_with_pad(image, image_size, image_size)
        elif image.shape[1] > max_dynamic_size or image.shape[2] > max_dynamic_size:
            image = tf.image.resize_with_pad(image, max_dynamic_size, max_dynamic_size)
        return image

    def _convert_image_to_array(self, jpg_image):
        """image: PIL.JpegImagePlugin.JpegImageFile"""
        """Returns: tf.python.framework.ops.EagerTensor"""
        jpg_image = np.array(jpg_image)
        # reshape into shape [batch_size, height, width, num_channels]
        img_reshaped = tf.reshape(jpg_image, [1, jpg_image.shape[0], jpg_image.shape[1], jpg_image.shape[2]])
        # Use `convert_image_dtype` to convert to floats in the [0,1] range.
        jpg_image = tf.image.convert_image_dtype(img_reshaped, tf.float32)
        return jpg_image

    def _make_prediction(self, image):
        model_handle = image_classification_models.model_handle_map[self._model_name]

        classifier = hub.load(model_handle)
        probabilities = tf.nn.softmax(classifier(image)).numpy()
        top_5 = tf.argsort(probabilities, axis=-1, direction="DESCENDING")[0][:5].numpy()

        # Some models include an additional 'background' class in the predictions, so
        # we must account for this when reading the class labels.
        includes_background_class = probabilities.shape[1] == 1001
        imagenet_classes = self._get_imagenet_classes()
        predictions = []
        for i, item in enumerate(top_5):
            class_index = item if not includes_background_class else item - 1
            predictions.append((imagenet_classes[class_index], probabilities[0][top_5][i]))

        return predictions

    def _get_imagenet_classes(self) -> List[str]:
        labels_file = "https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt"
        # Download labels and creates a maps
        downloaded_file = tf.keras.utils.get_file("labels.txt", origin=labels_file)
        classes = []
        i = 0
        with open(downloaded_file) as f:
            labels = f.readlines()
            classes = [l.strip() for l in labels[1:]]
            i += 1
        return classes


if __name__=='__main__':
    img_url = 'https://media.nationalgeographic.org/assets/photos/000/267/26734.jpg'
    user_agent = {'User-agent': 'Colab Sample (https://tensorflow.org)'}
    response = requests.get(img_url, headers=user_agent)
    image = Image.open(BytesIO(response.content))
    # ImageClassifier().get_descriptions(image).descriptions returns [('seashore', 0.99), ('beach', 0.77), ...]
    print(ImageClassifier().get_descriptions(image).descriptions)