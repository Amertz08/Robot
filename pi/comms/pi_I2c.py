import smbus
import time
import Rpi.GPIO as GPIO

from enum import Enum

class CardinalDirection(Enum):
    north = 'N'
    east = 'E'
    south = 'S'
    west = 'W'

class RelativeDirection(Enum):
    straight = 0
    right = 1
    left = 2
    reverse = 3

# for RPI version 1, use “bus = smbus.SMBus(0)”
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
sensorArduinoAddress = 10;

INTERRUPT_PIN = 17
current_orientation = CardinalDirection.north

direction_dict = {
    ('N', CardinalDirection.north): RelativeDirection.straight,
    ('N', CardinalDirection.east): RealativeDirection.left,
    ('N', CardinalDirection.south): RelativeDirection.reverse,
    ('N', CardinalDirection.west): RelativeDirection.right,
    ('E', CardinalDirection.north): RelativeDirection.right,
    ('E', CardinalDirection.east): RealativeDirection.straight,
    ('E', CardinalDirection.south): RelativeDirection.left,
    ('E', CardinalDirection.west): RelativeDirection.reverse,
    ('S', CardinalDirection.north): RelativeDirection.reverse,
    ('S', CardinalDirection.east): RealativeDirection.right,
    ('S', CardinalDirection.south): RelativeDirection.straight,
    ('S', CardinalDirection.west): RelativeDirection.left,
    ('W', CardinalDirection.north): RelativeDirection.left,
    ('W', CardinalDirection.east): RealativeDirection.reverse,
    ('W', CardinalDirection.south): RelativeDirection.right,
    ('W', CardinalDirection.west): RelativeDirection.straight
    }
def find_relative(next_direction):
    arduino_direction = direction_dict.get((next_direction, current_orientation))
    current_orientation = CardinalDirection(next_direction)
    return arduino_direction

def write_number(value):
    bus.write_byte(sensorArduinoAddress, value)
    # bus.write_byte_data(address, 0, value)
    return -1

def read_number():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

def read_barcode():
    camera = PiCamera()

    camera.start_preview(alpha=150)
    sleep(.5)
    camera.capture('/home/pi/Desktop/image.jpg')
    camera.stop_preview()

    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')   

    pil = Image.open('/home/pi/Desktop/image.jpg').convert('L')
    width, height = pil.size
    raw = pil.tobytes()

    my_stream = zbar.Image(width, height, 'Y800', raw) 

    scanner.scan(my_stream)
    # for symbol in my_stream:
    #     print('decoded', symbol.type, 'symbol', '"%s"' % symbol.data)
    return symbol.data

def my_callback(channel):
    # read QR from Camera
    barcode = read_barcode()
    # confirm correct node
    next_direction = #TODO
    # determine left right straight 
    arduino_direction = find_relative(next_direction)
    #tell arduino left right straight
    write_number(arduino_direction)
    return -1;

def main():
    #call route solver
    #
    GPIO.add_event_detect(INTERRUPT_PIN, GPIO.RISING, callback=my_callback)

if __name__ == '__main__':
    main()
