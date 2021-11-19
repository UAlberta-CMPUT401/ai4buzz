import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import json

class DendrogramGenerator: 
    def __init__(self):
        pass

    def generate(self, report):
        """ 
        generates a Dendrogram as an image object
        
        :param report: Dictionary of the feature analysis
        :returns type: Dendrogram
        """
        data = report
        num_images = len(data['feature_analysis_results'])
        total_data = np.zeros((num_images,10))
        for i in range(num_images):
  
            total_data[i][0] = (data['feature_analysis_results'][i]['color_scheme_analysis']['count'])
            total_data[i][1] = (data['feature_analysis_results'][i]['color_scheme_analysis']['colors'][0]['red'])
            total_data[i][2] = (data['feature_analysis_results'][i]['color_scheme_analysis']['colors'][0]['green'])
            total_data[i][3] = (data['feature_analysis_results'][i]['color_scheme_analysis']['colors'][0]['blue'])
            total_data[i][4] = (data['feature_analysis_results'][i]['sentiment_analysis']['sentiment_array[neg,neu,pos]'][0])
            total_data[i][5] = (data['feature_analysis_results'][i]['sentiment_analysis']['sentiment_array[neg,neu,pos]'][1])
            total_data[i][6] = (data['feature_analysis_results'][i]['sentiment_analysis']['sentiment_array[neg,neu,pos]'][2])

            if data['feature_analysis_results'][i]['text_recognition'] == "":
                total_data[i][7] = 0
            else:
                total_data[i][7] = 1

            object_keys = data['feature_analysis_results'][i]["object_detection"].keys()
            #print(object_keys)
            object_count = 0
            for key in object_keys:
                if key != 'processes_bounding_boxes_image_as_base64_string':
                    object_count = object_count + data['feature_analysis_results'][i]["object_detection"][key]["freq"] 
            total_data[i][8] = object_count

            total_data[i][9] = data['feature_analysis_results'][i]["face_analysis"]["count"]

        #print(total_data)
        #print(total_data.shape)

        for i in range(total_data.shape[1]):
            if total_data[:,i].max() != 0 :

                total_data[:,i] = total_data[:,i] / total_data[:,i].max()

        #print(total_data)
        #try cosine
        temp = hierarchy.linkage(total_data, 'single')
        plt.figure()
  
        dn = hierarchy.dendrogram(temp)
        plt.savefig('api/image_features/dendrogram_generator/dendrogram.png')


if __name__ == '__main__':
   
    with open('api/image_features/dendrogram_generator/7response.json') as f:
        data = json.load(f)

    #print(data['0'])
    gen = DendrogramGenerator()
    gen.generate(data)
    