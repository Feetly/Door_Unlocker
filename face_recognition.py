#https://github.com/syedhope/Face-Detection

# Import OpenCV2 for image processing
import cv2

# Import numpy for matrices calculations
import numpy as np

import os 

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

print("Recognition System activated : ")

# Create Local Binary Patterns Histograms for face recognization
recognizer = cv2.face.LBPHFaceRecognizer_create()

assure_path_exists("trainer/")

# Load the trained mode
recognizer.read('trainer/trainer.yml')

# Load prebuilt model for Frontal Face
cascadePath = "haarcascade_frontalface_default.xml"

# Create classifier from prebuilt model
faceCascade = cv2.CascadeClassifier(cascadePath);

# Set the font style
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize and start the video frame capture
cam = cv2.VideoCapture(0)

acc =0

# Loop
while True:
    # Read the video frame
    ret, im =cam.read()

    # Convert the captured frame into grayscale
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

    # Get all face from the video frame
    faces = faceCascade.detectMultiScale(gray, 1.2,5)

    # For each face in faces
    for(x,y,w,h) in faces:

        # Create rectangle around the face
        cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (255,255,0), 4)

        # Recognize the face belongs to which ID
        Id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        f=open("id.txt","r+")
	lines=f.readlines()
	face_id=int(lines[0])
	f.seek(len(lines[0]))
	n=lines[1].split()
	f.close()
	ch=[0]

        # Check the ID if exist 
        if(Id <= face_id and Id>0 and confidence<40):
            if(Id not in ch):
	        ch.append(Id) 
            Id = str(n[Id-1])
            acc = "{0:.2f}%".format(round(100 - confidence, 2))
        else:
            Id = "Unknown"
            acc = "0%"
	
        # Put text describe who is in the picture
        cv2.rectangle(im, (x-20,y-70), (x+w+20, y-20), (175,175,225), -1)
        cv2.putText(im, str(Id), (x-10,y-30), font, 1, (175,10,100), 3)
        cv2.putText(im, str(acc), (x,y+5), font, 0.7, (255,255,255), 3)

    # Display the video frame with the bounded rectangle
    cv2.imshow('im',im) 

    # If 'q' is pressed, close program
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Stop the camera
cam.release()

# Close all windows
cv2.destroyAllWindows()

try:
	if(len(ch)>0):
		print("We did Recognised "+str(len(ch))+" registered faces")
		print("Recognised Faces :- ")
		for i in ch:
			print("Name : "+str(n[i])+" & ID : "+str(i+1))
		print("Welcome! To the House\nDoor Unlocked Automatically")
	else:
		print("No Registered Face recognised.\nSorry Contact the House Owner to enter this house.\nDoor Still remains Looked")
except:
	pass

