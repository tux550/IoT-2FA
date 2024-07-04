from main import get_face_encodings
import json
import http

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

encodings = get_face_encodings()

# encodings = []

payload = {
    'name': name,
    'pin': pin,
    'face_encoding': encodings,
    'money':0
}

headers = {
    'Content-Type': 'application/json'
}

payload_str = json.dumps(payload)

conn.request("POST", "/user", body=payload_str, headers=headers)

# Get the response
response = conn.getresponse()
data = response.read()

print('Listo')
data = data.decode("utf-8")
# print(data)
data_dict = json.loads(data)

print(f'Se creo usuario con id {data_dict["id"]}')

