import serial
import time


def sensor_reading():
    port = "/dev/cu.usbmodem1411"
    baudrate = 9600
    # angle = [0, 90, 45, -45, "LCP", "RCP"]
    ser = serial.Serial(port, baudrate)

    time.sleep(2)

    ser.flush()
    ser.write('3')

    time.sleep(1)

    measurement = ser.readline()

    print "Voltage", measurement
