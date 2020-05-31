from gtts        import gTTS
from googletrans import Translator  
from os          import system
from time        import sleep, time 
from picamera    import PiCamera
import speech_recognition    as sr
import requests              as req
import xml.etree.ElementTree as ET
import numpy                 as np
import RPi.GPIO              as GPIO
import face_recognition
import pickle

camera          = PiCamera()
camera.rotation = 180
translator      = Translator()
keyword         = "hello"
directory       = "/home/pi/Desktop/SciRobot/"

def speech_recognition(lang):
	sample_rate = 48000
	device_id = 2
	chunk_size = 2048
	speech = ""	
	r = sr.Recognizer()
	with sr.Microphone(device_index = device_id, sample_rate = sample_rate,  
                        chunk_size = chunk_size) as source: 
		r.adjust_for_ambient_noise(source, duration = .5) 
		print("Say Something")
		audio = r.listen(source)      
		try: 
			speech = r.recognize_google(audio, language = lang) 
			print("you said: " + speech) 
		except sr.UnknownValueError: 
			speech = -1
			print("i could not understand you.")  
		except sr.RequestError as e: 
			speech = -1
			print("Request Error.")
	return speech

def answer(speech, lang):
	f = open("speech.txt")
	mytext = -1
	flg = 0
	for text in f:
		if flg:
			f.close()
			print(text)
			return text
		if text == speech + '\n':
			flg = 1
	f.close()
	mytext = web_search(speech)
	if mytext == "dont_know":
		mytext = "i don't know the answer yet. i will try to know the answer."
		speak(mytext, 'mb-us2')
		mytext = ""	
	elif mytext == "offline":
		mytext = "i am offline. i am trying to reconnect for you."
		speak(mytext, 'mb-us2')
		mytext = ""
	return mytext
	
def speak(speech, lang):
	speech = "'" + speech + "'"
	system("espeak -a 200 -g 5 -s 112 -v " + lang + " " + speech)
	
def web_search(speech):
	url = "http://api.wolframalpha.com/v2/query?input=" + speech + "&appid=KH88AY-V8X4LEXJV7&fbclid=IwAR0_L9b99_o4QT1lFc35E4vVMCXqLYsKK0SZ2EQA4p8lX68W8VduWcw0mhY&podindex=2"
	try:
		xml = req.get(url)
		root = ET.fromstring(xml.content)
		for child in root.iter('plaintext'):
			print(child.text)
			return child.text
		return "dont_know"
	except:
		return "offline"
	
def FACE_RECOGNITION():
	with open(directory + 'image/dataset_faces.dat', 'rb') as f:
		all_face_encodings = pickle.load(f)
	
	face_names = list(all_face_encodings.keys())
	face_encodings = np.array(list(all_face_encodings.values()))
	
	unknown_image = face_recognition.load_image_file(directory + "image/unknown.jpg")
	unknown_face = face_recognition.face_encodings(unknown_image, num_jitters = 10)
	try:
		result = face_recognition.compare_faces(face_encodings, unknown_face, tolerance = 0.5)
	except:
		mytext = "i coudn't recognize your face."
		speak(mytext, 'mb-us2')
		return "visitor"
	for i in range(len(result)):
		if result[i] == True:
			return face_names[i]
	return "visitor"
	
def capture_image(image_name):
	camera.start_preview()
	sleep(3)
	camera.capture(directory + "image/" + image_name + ".jpg", resize=(360, 360))
	camera.stop_preview()
	return 0

def museum_visit():
	system("feh -qrYzFD2 --on-last-slide=quit --auto-zoom fill /home/pi/Desktop/SciRobot/museum_image/")
		
def lighting(pin, state):
	if state == "ON":
		GPIO.output(pin, GPIO.HIGH)
	else:
		GPIO.output(pin, GPIO.LOW)
	
def main():
	system("pcmanfm --set-wallpaper='" + directory + "image/black.jpg'")
	flg = st = et = 0
	pin = 18
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)
	speech = ""
	
	while True:
		if speech != keyword:
			speech = speech_recognition('en-US')
		
		if speech == keyword:
			flg = 1
			
			lighting(pin, "ON")	
			
			capture_image("unknown")
			
			name = FACE_RECOGNITION()
				
			if name != "visitor":
				name = '_'.join(name.split())
				print(name)
				system("pcmanfm --set-wallpaper='" + directory + "image/" + name + ".jpg'")
			else:
				system("pcmanfm --set-wallpaper='" + directory + "image/unknown.jpg'")
			
			print(name)
			mytext = "Hi "
			mytext += name
			mytext += ", how can i help you?"
			speak(mytext, "mb-us2")
			
			system("rm " + directory + "image/unknown.jpg")
			lighting(pin, "OFF")
			
			speech = speech_recognition('en-us')
			
			st = time()
			
		if flg and speech != keyword:
			et = time()
			if et - st > 10:
				print(et-st, "secs without any question")
				flg = 0
				st = et = 0.00
				system("pcmanfm --set-wallpaper='" + directory + "image/black.jpg'")
				continue
				
			lighting(pin, "ON")
			
			if speech == -1:
				mytext = "may you please ask the question again?"
				speak(mytext, 'mb-us2')
			elif speech in ["Museum visit", "museum visit"]:
				museum_visit()
				st = time()
			else:
				mytext = answer(speech, 'en')
				#print(mytext)
				if mytext != "":
					speak(mytext, 'mb-us2')
				st = time()	
			
			lighting(pin, "OFF")
		
main()












