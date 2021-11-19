import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import json

class DendrogramGenerator: 
    def __init__(self):
        self.formatted_data = None
        self.data = None

    def generate(self, report):
        """ 
        generates a Dendrogram as an image object
        
        :param report: Dictionary of the feature analysis
        :returns type: Dendrogram
        """
        self.data = report
        num_images = len(self.data['feature_analysis_results'])
        self.formatted_data = np.zeros((num_images,10))
        for i in range(num_images):
  
            self.formatted_data[i][0] = (self.data['feature_analysis_results'][i]['color_scheme_analysis']['count'])
            self.formatted_data[i][1] = (self.data['feature_analysis_results'][i]['color_scheme_analysis']['colors'][0]['red'])
            self.formatted_data[i][2] = (self.data['feature_analysis_results'][i]['color_scheme_analysis']['colors'][0]['green'])
            self.formatted_data[i][3] = (self.data['feature_analysis_results'][i]['color_scheme_analysis']['colors'][0]['blue'])
            self.formatted_data[i][4] = (self.data['feature_analysis_results'][i]['sentiment_analysis']['sentiment_array[neg,neu,pos]'][0])
            self.formatted_data[i][5] = (self.data['feature_analysis_results'][i]['sentiment_analysis']['sentiment_array[neg,neu,pos]'][1])
            self.formatted_data[i][6] = (self.data['feature_analysis_results'][i]['sentiment_analysis']['sentiment_array[neg,neu,pos]'][2])

            if self.data['feature_analysis_results'][i]['text_recognition'] == "":
                self.formatted_data[i][7] = 0
            else:
                self.formatted_data[i][7] = 1

            object_keys = self.data['feature_analysis_results'][i]["object_detection"].keys()
            #print(object_keys)
            object_count = 0
            for key in object_keys:
                if key != 'processes_bounding_boxes_image_as_base64_string':
                    object_count = object_count + self.data['feature_analysis_results'][i]["object_detection"][key]["freq"] 
            self.formatted_data[i][8] = object_count

            self.formatted_data[i][9] = self.data['feature_analysis_results'][i]["face_analysis"]["count"]

        print(self.formatted_data)

        for i in range(self.formatted_data.shape[1]):
            if self.formatted_data[:,i].max() != 0 :

                self.formatted_data[:,i] = self.formatted_data[:,i] / self.formatted_data[:,i].max()

        print(self.formatted_data)
        #try cosine
        temp = hierarchy.linkage(self.formatted_data, 'single')
        plt.figure()
  
        dn = hierarchy.dendrogram(temp)
        plt.savefig('api/image_features/dendrogram_generator/dendrogram.png')

    #def add_colours(self)

if __name__ == '__main__':
   
    with open('api/image_features/dendrogram_generator/7response.json') as f:
        data = json.load(f)

    #print(data['0'])
    gen = DendrogramGenerator()
    gen.generate(data)
    