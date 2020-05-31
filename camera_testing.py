from picamera import PiCamera
from time import sleep

camera            = PiCamera()
camera.rotation   = 180
camera.brightness = 85
camera.contrast   = 85
camera.sharpness  = 50
camera.start_preview()
sleep(10)
camera.stop_preview()
camera.close()

