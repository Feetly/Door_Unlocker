#!/usr/bin/env python
# Import OpenCV2 for image processing
import cv2
import os
import time

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def main():

# Start capturing video 
	vid_cam = cv2.VideoCapture(0)

# Detect object in video stream using Haarcascade Frontal Face
	face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# For each person, one face id
	f=open("id.txt","r+")
	lines=f.readlines()
	face_id=int(lines[0])+1
	f.seek(0)
	f.write(str(face_id))
	f.seek(len(lines[0]))
	name=raw_input("%d. Name : "%(face_id))
	n=lines[1].split()
	n.append(name)
	n=" ".join(n)
	f.write(n)
	f.close()

# Initialize sample face image
	count = 0

	font = cv2.FONT_HERSHEY_SIMPLEX

	assure_path_exists("dataset/")

# Start looping
	while(True):

    # Capture video frame
	    _, image_frame = vid_cam.read()

    # Convert frame to grayscale
	    gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

    # Detect frames of different sizes, list of faces rectangles
	    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    # Loops for each faces
	    for (x,y,w,h) in faces:
	
        # Crop the image frame into rectangle
	        cv2.rectangle(image_frame, (x,y), (x+w,y+h), (255,255,0), 2)
	        cv2.putText(image_frame, "Loading "+str(name), (x,y-20), font, 1, (175,10,100), 3)
	        cv2.putText(image_frame, "Progress : "+str(count)+"%", (x+25,y+25), font, 0.7, (255,255,255), 3)
        
        # Increment sample face image
	        count += 1
	        time.sleep(0.2)

        # Save the captured image into the datasets folder
	        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        # Display the video frame, with bounded rectangle on the person's face
	        cv2.imshow('frame', image_frame)

    # To stop taking video, press 'q' for at least 100ms
	    if cv2.waitKey(100) & 0xFF == ord('q'):
	        print("Loading "+str(name)+" is not completed.\nProgress "+str(count)+"%")
	        break

    # If image taken reach 100, stop taking video
	    elif count>100:
	        print("Loading "+str(name)+" has been completed succesfully")
	        break

# Stop video
	vid_cam.release()

# Close all started windows
	cv2.destroyAllWindows()

print("Welcome to our Automatic Face Based Door Unlock System")
f=open("id.txt","r+")
lines=f.readlines()
face_id=int(lines[0])
f.close()
if(face_id==0):
	while(True):
		print("U have no Database, Dont worry will make one")
		print("Welcome to Face Recognition DataBase System\nFirstly We r going to collect database for yr house members")
		main();
		print("Do u want to still keep adding family member? (y or n)")
		if(raw_input()=="n"):			
			print("Database has been Upated Succesfully")
			break
else:
	print("U already have a Database.\nDo u wanna add new face? (y or n)")
	if(raw_input()=="y"):
		while(True):
			print("Welcome to Face Recognition DataBase System\nFirstly We r going to collect database for yr house members")
			main();
			print("Do u want to still keep adding family member? (y or n)")
			if(raw_input()=="n"):
				print("Database have been Updated Succesfully")
				break

