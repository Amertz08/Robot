import smbus
import time
import Rpi.GPIO as GPIO
# for RPI version 1, use “bus = smbus.SMBus(0)”
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
sensorArduinoAddress = 10;

INTERRUPT_PIN = 17
STRAIGHT = 0
LEFT = 1
RIGHT = 2

def writeNumber(value):
    bus.write_byte(sensorArduinoAddress, value)
    # bus.write_byte_data(address, 0, value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

def my_callback(channel):
    # read QR from Camera
    # confirm correct node
    # determine left right straight

    #tell arduino left right straight
    writeNumber()
    return -1;

GPIO.add_event_detect(INTERRUPT_PIN, GPIO.RISING, callback=my_callback)
