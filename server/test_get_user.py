from main import get_face_encodings_camera, get_most_close_user, mock_face_encodings
import json
import cv2

cap = cv2.VideoCapture(0)

cap.set(3, 640) # set Width
cap.set(4, 480) # set Height
# encodings = mock_face_encodings()
encodings = get_face_encodings_camera(cap)
result = get_most_close_user(json.dumps(encodings))

cap.release()