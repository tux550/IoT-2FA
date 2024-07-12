import serial
import json
import time
# http package
from PIL import Image
import http.client
import numpy as np
import cv2
import io

import face_recognition
from face_recognizer import face_recognition_fun, face_encodings_fun


def get_image():
    conn = http.client.HTTPConnection('192.168.225.111')

    # Send GET request
    conn.request("GET", "/capture")

    # Get the response
    response = conn.getresponse()

    # Check if the request was successful
    if response.status == 200:
        # Read the response body
        data = response.read()
        # parse data as numpy image array
        # data_io = io.BytesIO(data)

        # # Open the image data with PIL
        # image = Image.open(data_io)

        # # Convert the PIL image to a NumPy array
        # return np.array(image)
        nparr = np.frombuffer(data, np.uint8)

        # Decode the image data
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        return image
    else:
        print(f"Failed to get images: {response.status} {response.reason}")
        return None


def mock_face_encodings():

    vector = [-0.03095795,  0.10461359,  0.05317945,  0.01200438, -0.11492222,  0.02242018,
              -0.01956706, -0.05965982,  0.17701212, -0.15657477,  0.17493843,  0.02731113,
              -0.2235537,   0.0374266,  -0.03639125,  0.07442511, -0.08411667, -0.1031458,
              -0.12930991, -0.07837436,  0.04225795,  0.021482,   -0.00734988,  0.06419422,
              -0.07901341, -0.29345268, -0.09213012, -0.10066842,  0.10381235, -0.07655871,
              0.01328302, -0.01094132, -0.09384461,  0.04431884, -0.02361175,  0.02182499,
              -0.08976477, -0.05815402,  0.26252836, -0.03649428, -0.17914645,  0.04889312,
              0.04345325,  0.23605959,  0.17982586,  0.05043384,  0.03987253, -0.04756892,
              0.15019494, -0.2248542,   0.02221946,  0.17862272,  0.09274443,  0.13983724,
              0.09481744, -0.22584763,  0.01964105,  0.12362467, -0.18400545,  0.14644462,
              -0.04469081, -0.0940409,  -0.01614658, -0.00183595,  0.19974151,  0.10290138,
              -0.10607506, -0.14304756,  0.16519088, -0.27330226, -0.00816608,  0.14283592,
              -0.14428376, -0.19333152, -0.17641927,  0.0481671,   0.46128958,  0.19476137,
              -0.09044041,  0.02809368, -0.00436289, -0.0652731,   0.06952385,  0.08310937,
              -0.10345458, -0.09152536, -0.05976072,  0.0603464,   0.23248848, -0.01935552,
              -0.04124961,  0.21720845,  0.02403275,  0.04180107, -0.02798235,  0.01083204,
              -0.06732881, -0.01211136, -0.07099,     0.02818997,  0.01435616, -0.15014119,
              0.01453628, -0.0012428,  -0.18070641,  0.13987775, -0.01272655,  0.00743359,
              -0.02653906,  0.09383938, -0.17392614,  0.03829695,  0.23758395, -0.26695606,
              0.30808163,  0.19188039,  0.05280141,  0.12998465,  0.06447532,  0.07315391,
              0.0412778,  -0.05939937, -0.11442997, -0.08944571,  0.00468835, -0.06013031,
              0.06386436,  0.01938863]
    return vector


def get_most_close_user(face_encoding):
    conn = http.client.HTTPConnection('localhost:8000')

    conn.request("GET", "/user_search", body=face_encoding)

    response = conn.getresponse()

    if response.status == 200:
        data = response.read()
        return json.loads(data)
    else:
        print(f"Failed to get images: {response.status} {response.reason}")
        return None


def face_recognition_fun(frame, haar_cascade):

    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = haar_cascade.detectMultiScale(gray_img,
                                          scaleFactor=1.05,
                                          minNeighbors=1,
                                          minSize=(
                                              int(640 * 0.4),
                                              int(480 * 0.4))
                                          )
    max_area = -1
    cropped_image = [None]

    #print(faces)

    for x, y, w, h in faces:
        # crop the image to select only the face
        if w * h > max_area:
            max_area = w * h
            cropped_image[0] = frame[y: y + h, x: x + w]

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('frame', frame)

    return cropped_image[0]
# save face


def get_face_encodings():

    haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    while True:
        frame = get_image()

        face = face_recognition_fun(frame, haar_cascade)
        # cv2.imwrite('face.png', face)

        if face is not None:
            face_location = face_recognition.face_locations(face)
            face_encodings = face_encodings_fun(frame, face_location)

            if face_encodings == []:
                print("No se pudo conseguir encodings...", face_encodings)
            else:
                cv2.destroyAllWindows()
                return list(face_encodings[0])

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def get_face_encodings_camera(cap):
    haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cap.read()
        face = face_recognition_fun(frame, haar_cascade)
        if face is not None:
            face_location = face_recognition.face_locations(face)
            face_encodings = face_encodings_fun(frame, face_location)
            
            #print(face_encodings)
            #print(len(face_encodings))
            if face_encodings == []:
                print("No se pudo conseguir encodings...", face_encodings)
            else:
                cv2.destroyAllWindows()
                return list(face_encodings[0])

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


def verify_user_pin(id, pin):
    conn = http.client.HTTPConnection('localhost:8000')

    payload=json.dumps({"pin": pin, "id": id})
    print(payload)
    conn.request("POST", "/verify-pin",
                 body=payload)

    response = conn.getresponse()

    if response.status == 200:
        data = response.read()
        return json.loads(data)
    else:
        print(f"Failed to get images: {response.status} {response.reason}")
        return None

# encodings = mock_face_encodings()
# encodings = get_face_encodings()
# result = get_most_close_user(json.dumps(encodings))
# exit(0)

# print(result)


# Define serial port and baud rate
serial_port = 'COM7'
baud_rate = 115200

if __name__ == '__main__':
    # Establish serial connection
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    id = None

    try:
        # Wait for serial to initialize
        time.sleep(2)

        # Read and print data from Arduino indefinitely
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(f'SERIAL:"{line}"')

                if line == 'TAKE_IMAGE':
                    # face = get_image()

                    # cv2.imwrite('face.png', face)
                    # face_encoding = mock_face_encodings(face)

                    face_encoding = get_face_encodings()

                    print(f'JOB:"imagen obtenida"')

                    # face encoding to string
                    user_id = get_most_close_user(
                        json.dumps(face_encoding)
                    )


                    print(f'JOB:"usuario obtenido"')

                    if user_id is not None:
                        ser.write('ACCEPT\0'.encode())
                        id = user_id 
                        time.sleep(0.05)
                    else:
                        ser.write(b'REJECT')
                        time.sleep(0.05)
                elif line.startswith('PIN:'):
                    _, pin = line.strip().split(":")
                    ok = verify_user_pin(id, pin)

                    if ok:
                        ser.write('ACCEPT\0'.encode())
                        time.sleep(0.05)
                    else:
                        ser.write('REJECT\0'.encode())
                        time.sleep(0.05)
                elif line.startswith('FINGER:'):
                    trimmed_line = line.strip()
                    _, number = trimmed_line.split(':')
                    id = int(number)

    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        # Close serial connection
        ser.close()
