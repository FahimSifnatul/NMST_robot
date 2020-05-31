from gtts import gTTS

language = "en-us"
speech = "Sorry, I am offline. Please pardon me. I will try answer you when i am online again."
myobj = gTTS(text=speech, lang=language, slow=False) 
myobj.save("/home/pi/Desktop/SciRobot/offline.mp3") 
