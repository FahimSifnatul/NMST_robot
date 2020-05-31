import requests as req
from os import system

system("espeak -s 10 'wallie knows about weather.'")

url = 'https://api.openweathermap.org/data/2.5/weather?q=Dhaka,bd&appid=226961b129b160c9d22abc54f9f49030'
weather = (req.get(url)).json()
msg = "'Todays temperature is " + str(int(weather['main']['temp'])-273) + " degree celcius'"
system('espeak -s 10 ' + msg)

msg = "'pressure is " + str(weather['main']['pressure']) + " atm'"
system('espeak -s 10 ' + msg)

msg = "'humidity of air is " + str(weather['main']['humidity']) + " percent'"
system('espeak -s 10 ' + msg)

msg = "'wind speed is " + str(weather['wind']['speed']) + " meter per second at " + str(weather['wind']['deg']) + " degree.'"
system('espeak -s 10 ' + msg)

msg = "'Will Wallie go?'"
system("espeak -s 10 " + msg)











