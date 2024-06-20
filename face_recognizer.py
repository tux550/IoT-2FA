import cv2 
import numpy as np
import os
from PIL import Image
import face_recognition


def get_camera():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640) # set Width
    cap.set(4, 480) # set Height
    return cap


def face_recognition_fun(cap,frame, haar_cascade): 
    
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = haar_cascade.detectMultiScale(gray_img, 
                                          scaleFactor=1.05, 
                                          minNeighbors=1,                                           
                                          minSize = (
                                                    int(cap.get(3) * 0.4), 
                                                    int(cap.get(4) * 0.4))
                                        )
    max_area = -1
    cropped_image = [None]
    
    for x, y, w, h in faces:
        # crop the image to select only the face
        if w * h > max_area:
            max_area = w * h
            cropped_image[0] =  frame[y : y + h, x : x + w]
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('frame', frame)
        
    return cropped_image[0]

def face_encodings_fun(image, locations = None):
    face_encodings = face_recognition.face_encodings(image, locations)
    return face_encodings


if __name__ == '__main__': 
    
    cam = get_camera()
    haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    while True:
        ret, frame = cam.read()
        face = face_recognition_fun(cam, frame, haar_cascade)
        
        if face is not None:            
            face_location = face_recognition.face_locations(face)
            face_encodings = face_encodings_fun(frame, face_location)
            if face_encodings == []:
                print("No face found")
            else:  
                print(face_encodings[0])
        
        
        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cam.realease()
    cv2.destroyAllWindows()









