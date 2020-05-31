from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation   = 180
camera.brightness = 75
camera.contrast   = 75
camera.sharpness  = 50
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
def capture_image():
	camera.start_preview()
	sleep(3)
	camera.capture("/home/pi/Desktop/SciRobot/image/mister_fahim_sifnatul_1.jpg", resize = (480, 360))
	camera.stop_preview()

capture_image()
