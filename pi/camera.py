from picamera import PiCamera
from time import sleep
import zbar
print("zbar")
import Image

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