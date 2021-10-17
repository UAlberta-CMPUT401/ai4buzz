import cv2
import sys

#image file as a command line argument
imagePath = sys.argv[1]

image = cv2.imread(imagePath)

#turn picture into grayscale for more optimal results
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#creating a Haar cascade that includes pre-trained classifiers
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

#generates a list of rectangles for all detected faces from the Haar cascade in the form of Rect(x, y, w, h)
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.3,
    minNeighbors=3,
    minSize=(30, 30)
)

print("Found", len(faces), "faces!")

#drawing rectangle around the coordinates provided in the list of rectanges previously generated
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

#if you want to see the new image with the expected outlines for each face, uncomment following section
#will write new image into a .png file called faces_detected in your current directory
# status = cv2.imwrite('faces_detected.jpg', image)

#status message checker to determine if an error occurs when writing the new file
#print("[INFO] Image faces_detected.jpg written to filesystem: ", status)


