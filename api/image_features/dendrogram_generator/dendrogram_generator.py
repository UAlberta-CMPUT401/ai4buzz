import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import json
from PIL import Image 

class DendrogramGenerator: 
    def __init__(self):
        self.formatted_data = []
        self.data = None
        self.Image_IDs = []
        self.image_results = []

    def add_color_analysis(self, i):
        #Add colour results from current image to array
        self.image_results.append(self.data[i]['color_scheme_analysis']['count'])
        #RGB values from colour with the highest proportion in the image since that is the only thing that stays the same between images
        self.image_results.append(self.data[i]['color_scheme_analysis']['colors'][0]['red'])
        self.image_results.append(self.data[i]['color_scheme_analysis']['colors'][0]['green'])
        self.image_results.append(self.data[i]['color_scheme_analysis']['colors'][0]['blue'])

    def add_sentiment_analysis(self, i):
        #Add sentiment from current image to array 
        self.image_results.append(self.data[i]['sentiment_analysis']['sentiment_array[neg,neu,pos]'][0])
        self.image_results.append(self.data[i]['sentiment_analysis']['sentiment_array[neg,neu,pos]'][1])
        self.image_results.append(self.data[i]['sentiment_analysis']['sentiment_array[neg,neu,pos]'][2])
    
    def add_text_analysis(self, i):
        # If there is text detected set value to 1, if not set to 0 and add to array, this binary way is the easiest way to compare text
        #  if there is another numerical method to compare strings in a meaningful way, it could be implemented here.
        if self.data[i]['text_recognition'] == "":
            self.image_results.append(0)
        else:
            self.image_results.append(1)

    def add_object_analysis(self,i):
        #Count number of objects and add to array
        # Number of objects is the only thing that is always in the analysis.
        # If certain objects are detected could also be added to the array in the future
        object_keys = self.data[i]["object_detection"].keys()
        object_count = 0
        for key in object_keys:
            if key != 'processes_bounding_boxes_image_as_base64_string':
                object_count = object_count + self.data[i]["object_detection"][key]["freq"] 
        self.image_results.append(object_count)

    def add_facial_analysis(self,i):
        #add results from facial analysis to the array
        #Since the number of faces changes the number of faces is the easiest way to compare the different images
        self.image_results.append(self.data[i]["face_analysis"]["count"])

    def normalize_array(self):
        # normalize data in each category to between 0 and 1
        
        for i in range(self.formatted_data.shape[1]):
            if self.formatted_data[:,i].max() != 0 :
                # The weights for each category of data can be changed by multiplying the right side of the equation depending on the step
                self.formatted_data[:,i] = self.formatted_data[:,i] / self.formatted_data[:,i].max()


    def generate(self, report):
        """ 
        generates a Dendrogram as an image object
        
        :param report: Dictionary of the feature analysis
        :returns type: Dendrogram
        """
        self.data = report
        num_images = len(self.data)
        #self.formatted_data = np.zeros((num_images,10))

        #runs through each images and records the data into a numpy array
        for i in range(num_images):
            #set labels
            self.Image_IDs.append(self.data[i]["id"])
            self.image_results = []

            self.add_color_analysis(i)
            self.add_sentiment_analysis(i)
            self.add_text_analysis(i)
            self.add_object_analysis(i)
            self.add_facial_analysis(i)

            #append data to list of images
            self.formatted_data.append(self.image_results)

        
        self.formatted_data = np.asarray(self.formatted_data)
        

        self.normalize_array()
        #print(self.formatted_data)

        #try cosine or euclidian 
        #Generate dendrogram
        temp = hierarchy.linkage(self.formatted_data, 'single')
        plt.figure()
        dn = hierarchy.dendrogram(temp, labels=self.Image_IDs,leaf_font_size=5)
        plt.savefig('api/image_features/dendrogram_generator/dendrogram.png')

        return Image.open('api/image_features/dendrogram_generator/dendrogram.png')



if __name__ == '__main__':
   
    with open('api/image_features/dendrogram_generator/7response.json') as f:
        data = json.load(f)

    #print(data['0'])
    gen = DendrogramGenerator()
    gen.generate(data['feature_analysis_results'])
    