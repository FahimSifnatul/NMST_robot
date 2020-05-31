from gtts        import gTTS
from googletrans import Translator  
from os          import system
from time        import sleep 
from picamera    import PiCamera
import speech_recognition    as sr
import requests              as req
import xml.etree.ElementTree as ET
import numpy                 as np
import RPi.GPIO              as GPIO
#import face_recognition
import pickle

camera     = PiCamera()
translator = Translator()
pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)

def keyword_detection():
	key = speech_recognition("en-US")
	return (1 if key == "hi Prime" else 0)

def speech_recognition(lang):
	sample_rate = 48000
	device_id = 2
	chunk_size = 2048
	speech = ""	
	r = sr.Recognizer()
	with sr.Microphone(device_index = device_id, sample_rate = sample_rate,  
                        chunk_size = chunk_size) as source: 
		r.adjust_for_ambient_noise(source) 
		print("Say Something")
		audio = r.listen(source)      
		try: 
			speech = r.recognize_google(audio, language = lang) 
			print("you said: " + speech) 
		except sr.UnknownValueError: 
			speech = -1
			print("Prime could not understand audio")  
		except sr.RequestError as e: 
			speech = -1
			print("Request Error.")
	return speech

def translation(speech, lang):
	return (translator.translate(speech, dest = lang)).text

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
	if lang == 'bn':
		speech = translation(speech, 'en')
	mytext = web_search(speech)
	if mytext == "":
		system("mpg321 dont_know.mp3")	
	return mytext
	
def speak(speech, lang):
	try:
		myobj = gTTS(text=speech, lang=lang, slow=False) 
		myobj.save("answer.mp3") 
		system("mpg321 answer.mp3")
		system("rm answer.mp3")	
	except:
		system("mpg321 offline.mp3")

def web_search(speech):
	url = "http://api.wolframalpha.com/v2/query?input=" + speech + "&appid=KH88AY-V8X4LEXJV7&fbclid=IwAR0_L9b99_o4QT1lFc35E4vVMCXqLYsKK0SZ2EQA4p8lX68W8VduWcw0mhY&podindex=2"
	try:
		xml = req.get(url)
		root = ET.fromstring(xml.content)
		for child in root.iter('plaintext'):
			print(child.text)
			return child.text
		return ""
	except:
		return "Sorry, I am offline. Please pardon me. I will try to answer you when i am online again."
	
def FACE_RECOGNITION():
	with open('/home/pi/Desktop/SciRobot/image/dataset_faces.dat', 'rb') as f:
		all_face_encodings = pickle.load(f)
	
	face_names = list(all_face_encodings.keys())
	face_encodings = np.array(list(all_face_encodings.values()))
	
	unknown_image = face_recognition.load_image_file("unknown.jpg")
	unknown_face = face_recognition.face_encodings(unknown_image)
	try:
		result = face_recognition.compare_faces(face_encodings, unknown_face, tolerance = 0.5)
	except:
		speech = "দুঃখিত, আমি আপনার মুখ শনাক্ত করতে  পারিনি"
		print(speech)
		speak(speech)
		return "দর্শনার্থী"
	for i in range(len(result)):
		if result[i] == True:
			return face_names[i]
	return "দর্শনার্থী"
	
def capture_image(image_name):
	camera.start_preview()
	sleep(5)
	camera.capture(image_name + ".jpg", resize=(240, 240))
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
	while True:
		if keyword_detection():
			global pin 
			lighting(pin, "ON")	
			
			'''capture_image("unknown")
			
			name = FACE_RECOGNITION()
			
			if name != "দর্শনার্থী":
				tmp_name = '_'.join(name.split())
				print(tmp_name)
				system("pcmanfm --set-wallpaper='/home/pi/Desktop/SciRobot/image/" + tmp_name + ".jpg'")
			else:
				system("pcmanfm --set-wallpaper='/home/pi/Desktop/SciRobot/unknown.jpg'")
			
			name = translation(name, 'bn')		
			greeting = "প্রিয় " + name + ", আমি কি আপনাকে সাহায্য করতে পারি?
			print(greeting)
			speak(greeting)
			
			system("rm unknown.jpg")'''
			
			speech = speech_recognition('bn-BD')
			
			if speech == -1:
				speak("দুঃখিত, আমি আপনার প্রশ্ন বুঝতে পারিনি। অনুগ্রহপূর্বক আবার জিজ্ঞাসা করুন")
			elif speech in ["জাদুঘর পরিদর্শন", "যাদুঘর পরিদর্শন"]:
				museum_visit()
			else:
				mytext = answer(speech, 'bn')
				mytext = translation(mytext, 'bn')
				print(mytext)
				speak(mytext, 'bn')
			
			system("pcmanfm --set-wallpaper='/home/pi/Desktop/SciRobot/image/black.jpg'")
			
			lighting(pin, "OFF")
		
main()































