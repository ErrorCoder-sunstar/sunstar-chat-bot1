#this is for face unlock feature in friday 
import face_recognition
import cv2
import numpy as np
from friday import TaskExecution


video = cv2.VideoCapture(0)

face = face_recognition.load_image_file("a2.jpg")
faceencoding = face_recognition.face_encodings(face)[0]

face_encodings_list = [
    faceencoding]

face_encodings = []
s = True
face_coordinates = []


while True:
    _,frame = video.read()
    
    resized_frame = cv2.resize(frame,(0,0),fx=0.25)
    
    resized_frame_rgb = resized_frame[:, :, ::-1]
    
    
    if s:
        face_coordinates = face_recognition.face_locations(resized_frame_rgb)
        face_encodings = face_recognition.face_encodings(resized_frame_rgb, face_coordinates)
        
        for faces in face_encodings:
            matches = face_recognition.compare_faces(face_encodings_list, faces)
            if matches[0] == True:
                video.release()
                cv2.destroyAllWindows()
                TaskExecution()
                
    cv2.imshow('Face Scan', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows