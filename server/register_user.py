from main import get_face_encodings,get_face_encodings_camera
import json
import http
import time
import cv2

conn = http.client.HTTPConnection('localhost:8000')


name = input('Ingrese su nombre: ')
pin = ''

while True:
    pin = input('Ingrese su pin: ')

    if len(pin) != 4:
        print("El pin tiene que tener longitud 4")
    else:
        break
print('Consiguiendo imagen...')

# encodings = get_face_encodings()
number_of_photos = 5
encodings = []

cap = cv2.VideoCapture(0)

cap.set(3, 640) # set Width
cap.set(4, 480) # set Height

for _ in range(number_of_photos):
    encodings.append(get_face_encodings_camera(cap))
    print(f"Foto {_+1}tomada ")
    time.sleep(1)

cap.release()   
# encodings = []

payload = {
    'name': name,
    'pin': pin,
    'face_encoding': json.dumps(encodings),
    'money':0
}



headers = {
    'Content-Type': 'application/json'
}

payload_str = json.dumps(payload)
# print(payload_str)

conn.request("POST", "/user", body=payload_str, headers=headers)

# Get the response
response = conn.getresponse()
data = response.read()

print('Listo')
data = data.decode("utf-8")
# print(data)
data_dict = json.loads(data)

print(f'Se creo usuario con id {data_dict["id"]}')

