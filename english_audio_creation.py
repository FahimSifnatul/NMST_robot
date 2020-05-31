from gtts import gTTS
from os import system

speech = "i am nick. but i have another cute name mean given by my master muhammad munir chowdhury sir who loves me very much."

myobj = gTTS(text=speech, lang='en', slow=False) 
myobj.save("audio/off_1.mp3") 

