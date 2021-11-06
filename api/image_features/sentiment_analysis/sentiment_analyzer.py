"""
Module containing class to analyze and classify sentiments in image

"""

# import sys
# sys.path.insert(0,'C:/Users/Joy/UofA-Drive/Fall-2021/CMPUT-401/Project/ai4buzz')
# model_path = 'vgg19_finetuned_all.pth'

model_path = 'api/image_features/sentiment_analysis/vgg19_finetuned_all.pth'
from api.image_features.sentiment_analysis.vgg19 import KitModel as VGG19
from api.image_features.feature_analyzer import FeatureAnalyzer

import torch
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import numpy as np
import matplotlib.pyplot as plt
import requests
from io import BytesIO


class ImageListDataset(Dataset):
    """
    Class for generating map-style testing image dataset
    """

    def __init__(self, ImageList, transform=None):
        super(ImageListDataset).__init__()
        self.list = ImageList
        self.transform = transform
        
    def __getitem__(self, index):
        x = self.list[index]
        if self.transform:
            x = self.transform(x)
        return x
    
    def __len__(self):
        return len(self.list)


class SentimentAnalyzer(FeatureAnalyzer):
    """
    Class for analyzing and classifying sentiments(negative, neutral, positive) 
    present in image using VGG19 pytorch model(https://pytorch.org/hub/pytorch_vision_vgg/)
    trained on ILSVRC12 dataset(https://image-net.org/challenges/LSVRC/2012/) and then finetuned on T4SA dataset(http://www.t4sa.it/)
    """

    def __init__(self, batch_size):
        self.description_dict = {}
        self.image_ID = 0
        self.batch_size = batch_size
        self.device = torch.device("cpu")
        self.model = VGG19(model_path).to(self.device)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Lambda(lambda x: x[[2,1,0], ...] * 255),  # RGB -> BGR and [0,1] -> [0,255]
            transforms.Normalize(mean=[116.8007, 121.2751, 130.4602], std=[1,1,1])  # mean subtraction
            ])

    def get_descriptions(self, ImageList):
        """
        Method for evaluating pytorch Model on testing image dataset 
        using torch.no_grad() in pair with model.eval() 
        to turn off gradients computation
        """

        dataset = ImageListDataset(ImageList, self.transform)
        dataloader = DataLoader(dataset, self.batch_size, num_workers=0)

        self.model.eval()
        with torch.no_grad():
            for batch_idx, data in enumerate(dataloader):
                output = self.model(data.to(self.device))  # order is (NEG, NEU, POS)
                # _, pred_idx = torch.max(output, dim=1)
                # print("\n\n", output, pred_idx)

                for i in range(data.shape[0]):
                    self.image_ID = i + batch_idx * self.batch_size
                    self._format_description(output[i].tolist())
                    # plt.imshow(ImageList[self.image_ID])
                    # plt.title(str(self.description_dict["image_"+str(self.image_ID+1)]["degrees"]))
                    # plt.show()

        return self.description_dict

    def _format_description(self, description):
        """
        Method for format the description of the sentiment analysis result
        """

        self.description_dict["image_"+str(self.image_ID+1)] = {}
        
        self.description_dict["image_"+str(self.image_ID+1)]["sentiment_array[neg,neu,pos]"] = description

        degrees_dict = {}
        for i in range(len(description)):
            if i == 0:
                degrees_dict["Negative"] = '{:.2%}'.format(description[i])
            elif i == 1:
                degrees_dict["Neutral"] = '{:.2%}'.format(description[i])
            elif i == 2:
                degrees_dict["Postive"] = '{:.2%}'.format(description[i])
        
        self.description_dict["image_"+str(self.image_ID+1)]["degrees"] = degrees_dict


if __name__=='__main__':
    image_path = 'https://www.gannett-cdn.com/media/2019/06/07/USATODAY/usatsports/america-fought-two-wars.jpg'
    response = requests.get(image_path)
    ImageList = [Image.open(BytesIO(response.content))]
    print(SentimentAnalyzer(batch_size=1).get_descriptions(ImageList))
