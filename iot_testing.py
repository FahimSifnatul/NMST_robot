import RPi.GPIO as gpio
import requests as req
import time

gpio.setmode(gpio.BOARD)

pin = 11
gpio.setup(pin, gpio.OUT)
gpio.output(pin, gpio.LOW)

ret = req.post('http://things.ubidots.com/api/v1.6/devices/iot_testing/?token=A1E-DsK2J8ZJ96sJPc7yIcTkFWIH230uPo', data={'gpio_pin_status':gpio.input(pin)})
print('Alhamdulillah.')

gpio.cleanup()
    









