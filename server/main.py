import serial
import time

# Define serial port and baud rate
serial_port = 'COM7'
baud_rate = 115200

# Establish serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

try:
    # Wait for serial to initialize
    time.sleep(2)

    # Read and print data from Arduino indefinitely
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)

            if line == 'TAKE_IMAGE':
                ser.write(b'ACCEPT')
            if line.startswith('PIN:'):
                ser.write(b'ACCEPT')

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    # Close serial connection
    ser.close()
