"""
Tests for Sentiment Analyzer Model

4 of the 5 unit tests utilizes a test suite for pytorch from https://github.com/suriyadeepan/torchtest
"""

# ### For local running
# import sys
# sys.path.insert(0,'C:/Users/Joy/UofA-Drive/Fall-2021/CMPUT-401/Project/ai4buzz')
# model_path = 'vgg19_finetuned_all.pth'

import gdown, os.path
model_url = 'https://drive.google.com/uc?id=1SwbKfAUFWUvJ1vQG9jFLBarcNuSeLelH'
model_path = 'api/image_features/sentiment_analysis/vgg19_finetuned_all.pth'
if not os.path.exists(model_path):
    gdown.download(model_url, model_path)

from PIL import Image
from unittest import TestCase
import unittest
import numpy
import torch
import torch.nn.functional as F
from torch.autograd import Variable
from torchtest import test_suite

from api.image_features import descriptions
from api.image_features.sentiment_analysis.sentiment_analyzer import SentimentAnalyzer
from api.image_features.sentiment_analysis.vgg19 import KitModel as VGG19

class SentimentAnalyzerTest(TestCase):

    batch_size = 5
    device = torch.device("cpu")
    inputs = Variable(torch.randn(batch_size, 3, 224, 224))
    targets = Variable(torch.randint(0, 2, (batch_size,))).long()
    batch = [inputs, targets]
    model = VGG19(model_path).to(device)

    def test_vars_change(self):
        """
        This unit test validates if the model parameters (params) DO change during training
        """
        test_suite(
            model=SentimentAnalyzerTest.model,
            loss_fn=F.cross_entropy,
            optim=torch.optim.Adam(SentimentAnalyzerTest.model.parameters()),
            batch=SentimentAnalyzerTest.batch,
            device=SentimentAnalyzerTest.device,
            test_vars_change=True)
    
    def test_nan_vals(self):
        """
        This unit test checks presence of NaN values
        """
        test_suite(
            model=SentimentAnalyzerTest.model,
            loss_fn=F.cross_entropy,
            optim=torch.optim.Adam(SentimentAnalyzerTest.model.parameters()),
            batch=SentimentAnalyzerTest.batch,
            device=SentimentAnalyzerTest.device,
            test_nan_vals=True)

    def test_inf_vals(self):
        """
        This unit test checks presence of inf values
        """
        test_suite(
            model=SentimentAnalyzerTest.model,
            loss_fn=F.cross_entropy,
            optim=torch.optim.Adam(SentimentAnalyzerTest.model.parameters()),
            batch=SentimentAnalyzerTest.batch,
            device=SentimentAnalyzerTest.device,
            test_inf_vals=True)


    def test_output_range(self):
        """
        This unit test checks if Softmax output range within [0,1].
        """
        test_suite(
            model=SentimentAnalyzerTest.model,
            loss_fn=F.cross_entropy,
            optim=torch.optim.Adam(SentimentAnalyzerTest.model.parameters()),
            batch=SentimentAnalyzerTest.batch,
            device=SentimentAnalyzerTest.device,
            test_output_range=True,
            output_range=(0, 1))


    def test_description_len(self):
        """
        This unit test checks if the model returns output with required length 3 [neg,neu,pos].
        """
        a = numpy.random.rand(224,224,3) * 255
        mock_image = Image.fromarray(a.astype('uint8')).convert('RGB')  # Random image

        sentiment_analyzer = SentimentAnalyzer(batch_size=1)
        actual_description_len = len(sentiment_analyzer.get_descriptions([mock_image])['sentiment_array[neg,neu,pos]'])   
        self.assertEqual(actual_description_len, 3)

        

if __name__ == '__main__':
    unittest.main()
    
