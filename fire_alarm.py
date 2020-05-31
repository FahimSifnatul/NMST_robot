import requests as req
from time import sleep
from os import system

url = 'http://things.ubidots.com/api/v1.6/devices/office_assistant_robot/?token=A1E-DsK2J8ZJ96sJPc7yIcTkFWIH230uPo'
ret = req.post( url , data={'fire_status' : 1})

for i in range(0,3):
	system("espeak -s 10 'Hurry up. hurry up. Walle detected fire. Use the emergency door.'")



