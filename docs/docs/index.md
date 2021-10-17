# Project Requirements

## Executive Summary

This project is to develop a web service to allow researchers to gain insight into the meanings and semantics of what makes a social media post more influential. Specifically, this project will expose a web REST API to allow researchers at AI4Society to upload images and retrieve a summary of an analysis of that photo. This analysis may contain anything from a color scheme analysis to sentiment classification of the photo.

## Project Glossary

- **AI4Society** One of the five Signature Areas of Research and Teaching of the University of Alberta, and is focused on Artificial Intelligence, its applications, and its transformative role for our society.
- **Sentiment Analysis** The process of computational analysis to identify and categorize a particular photos attitude/sentiment.
- **Dendrogram** a tree diagram, especially one showing taxonomic relationships.
- **Base 64** Base64 is a binary to a text encoding scheme that represents binary data in an ASCII string format. It is designed to carry data stored in binary format across the network channels.
- **Batch processing** When data is processed in large quantities (e.g. uploading a large amount of files) within a certain timespan where the amount of data provided is finite and known beforehand. The results are then provided after the job is completed.
- **Streaming processing** This is when data is streamed to the system in real time; the analysis of each data inputted should be returned after a few milliseconds/seconds. The amount of data is not known beforehand and can theoretically be infinite and thus the input graph is dynamic rather than static.
- **Convolution neural network** A class of artificial neural networks used in image recognition that is specifically used to process pixel data.
- **Dense Classifier** In a neural network, each node in each layer (except for the input layer) is connected to each of the nodes in the previous layer, hence making it dense.
- **Web user** User accessing the website and its features from the frontend web client.
- **Researcher** a researcher is a user from AI4Society gaining information about images.

## User Stories

### US 1.01 - Image upload

> **As** a researcher, **I want** to upload one or many images using a web API, **so that** the images can be analyzed

> **Acceptance Tests**

> 1. Expose endpoint that allows for the upload of a base 64 encoded image
> 2. Expose endpoint that allows for the upload of multiple base 64 encoded image
> 3. Throw an error if the user tries to send data that is not of the expected format

### US 1.02 - Analysis response

> **As** a researcher, **I want** to retrieve the results of the analysis using a web API, **so that** I can run my own analysis on the results

> **Acceptance Tests**

> 1. Return analysis of the results in JSON format as a response to an image upload request

### US 1.03 - Generate Dendrogram

> **As** a researcher, **I want** to retrieve a dendrogram of a batch of images using a web API **so that** I can further understand the images

> **Acceptance Tests**

> 1. Return dendrogram as a base 64 encoded string as a response to a dendrogram request

### US 1.04 - Generate collage

> **As** a researcher, **I want** to retrieve a collage of images using a web API **so that** I can further understand them.

> **Acceptance Tests**

> 1. Return collage as a base 64 encoded string as a response to a dendrogram request

### US 1.05 - Colour scheme analysis

> **As** a researcher, **I want** to get the colour scheme analysis of an image **so that** I can know how color affects popularity of an image.

> **Acceptance Tests**

> 1. Given an image, return colour scheme analysis in response body of image upload request

### US 1.06 - Image sentiment classification

> **As** a researcher, **I want** to get the sentiment classification of an image **so that** I can know the mood of the image.

> **Acceptance Tests**

> 1. Given an image, return the sentiment of the image as a string
> 2. Need to ensure 70-80% accuracy

### US 1.07 - Object detection

> **As** a researcher, **I want** to be able to know the objects detected in a photo **so that** I can know the contents of the image.

> **Acceptance Tests**

> 1. Returns the number of objects in photo
> 2. Return the bounding box coordinates of those objects in the image
> 3. Return labels of those objects
> 4. Need to ensure 80-90% accuracy

### US 1.08 - Facial Detection

> **As** a researcher, **I want** to be able to know the number of faces detected in a photo **so that** I can know how the number of people affects popularity.

> **Acceptance Tests**

> 1. Returns the number of faces in photo
> 2. Return the bounding box coordinates of those faces in the image
> 3. Need to ensure 80-90% accuracy

### US 1.09 - Text extraction

> **As** a researcher, **I want** to be able to know if an image contains text and what that text is **so that** I can analyze the text in the image.

> **Acceptance Tests**

> 1. Extracts text from an image
> 2. Need to ensure 80-90% accuracy

### US 1.10 - Image Streaming

> **As** a researcher, **I want** to be able to stream images to a web service, **so that** I can get analysis in real time.

> **Acceptance Tests**

> 1. Allow client to initialize a connection to the web service over a streaming protocol
> 2. Allow for images to be streamed to backend and results to be streamed back

### US 1.11 - Text Detection

> **As** a researcher, **I want** to detect if an image has text in it **so that** I can analyze the impact the presence of text has in an images popularity

> **Acceptance Tests**

> 1. Model correctly detects whether there is text in an image or not
> 2. Ensure model accuracy better than 80%

### US 2.01 - Web client image upload

> **As** a web user, **I want** to upload one or many images, **so that** the images can be analyzed

> **Acceptance Tests**

> 1. Allow user to select images by selecting a single image or directory of images from their local machine to upload
> 2. Ensure that image(s) are uploaded as base 64 strings

### US 2.02 - Web client analysis

> **As** a web user, **I want** to view the results of the analysis, **so that** I can see the features about an image to gain understanding about it.

> **Acceptance Tests**

> 1. List the results of the analysis beside the image(s) that were uploaded
> 2. Allow user to browse through the uploaded images and their results by scrolling through or clicking through the images

### US 2.03 - Web client view collage

> **As** a web user, **I want** to view a collage of the images **so that** I can do aggregate analysis.

> **Acceptance Tests**

> 1. Ensure that collage renders properly on the frontend client
> 2. On clicking a button, the collage should render

### US 2.04 - Web client View Dendrogram

> **As** a web user, **I want** to view a dendrogram of the images **so that** I can understand the relationship between them.

> **Acceptance Tests**

> 1. Need to ensure dendrogram is rendered on the frontend client on click of a button
> 2. Need to ensure dendrogram is rendered correctly

### US 2.05 - Web client authentication

> **As** a web user, **I want** to authenticate with my email **so that** I can access the website and its features.

> **Acceptance Tests**

> 1. If user inputs correct info, it allows them onto the website
> 2. If the user inputs incorrect information, it declines entry onto website


### US 2.06 - Web client JSON download

> **As** a web user, **I want** to be able to generate an entire report of the features above in a JSON file, **so I** can use the file to do additional analysis.

> **Acceptance Tests**

> 1. Allow web user to download the report as a json file on click of a download button
> 2. Ensure that user can only request a download if they have uploaded an image(s) for analysis



## MoSCoW

### Must Have

- US 1.01 - Image upload in batches
- US 1.02 - Image analysis
- US 1.05 - Color scheme analysis
- US 1.06 - Image sentiment classification
- US 1.07 - Object detection
- US 1.08 - Facial detection
- US 1.11 - Text Detection

### Should Have

- US 2.01 - Webclient image upload
- US 2.02 - Webclient analysis
- US 2.03 - Web client view collage
- US 2.04 - Web client view dendrogram
- US 2.05 - Web client authentication
- US 2.06 - Web client JSON download
- US 1.04 - Generate Collage

### Could Have

- US 1.10 - Image Streaming
- US 1.03 - Generate Dendrogram
- US 1.09 - Text extraction

### Would Like but Won’t get

- None

## Similar Products

- [Google Vision AI API](https://cloud.google.com/vision)

  - Cloud based image detection and classification service.
  - The “Try me” section of the page has a simple and nice UI which we will draw inspiration from
  - The response schema is also something that we might draw inspiration from

- [Image Tagging API](https://imagga.com/solutions/auto-tagging)
  - A service that provides object detection and assignment of relevant tags to vast collections of data and object detection of 3000 everyday objects to images

## Open-Source Projects

- [Tensor Flow Hub](https://tfhub.dev/)
  - Hub for pre-trained TensorFlow Models
  - Might browse the pre-trained models offered and tweak some to fit our needs

## Technical Resources

### Machine Learning:

- [OpenCV Documentation](https://opencv.org/)
- [Scikit-image Documentation](https://scikit-image.org/)
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Keras Documentation](https://keras.io/)
- [Pytorch Documentation](https://pytorch.org/)

### Backend: FastAPI + PostgreSQL

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/docs/)

### Frontend: React

- [React Documentation](https://reactjs.org/)

### Deployment: Docker

- [Deploy FastAPI with Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Get started with docker](https://docs.docker.com/)
