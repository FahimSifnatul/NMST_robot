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
import json
import wikipediaapi

translator      = Translator()
keyword         = "hello Nick"
directory       = "/home/pi/SciRobot/"

def speech_recognition(lang):
	sample_rate = 48000
	device_id = 2
	chunk_size = 2048
	speech = ""	
	r = sr.Recognizer()
	with sr.Microphone(device_index = device_id, sample_rate = sample_rate,  
                        chunk_size = chunk_size) as source: 
		r.adjust_for_ambient_noise(source, duration = 1) 
		print("Say Something")
		audio = r.listen(source)      
		try: 
			speech = r.recognize_google(audio, language = lang) 
			print("you said: " + speech) 
		except sr.UnknownValueError: 
			speech = -1
			print("i could not understand you.")  
			system("mpg321 " + directory + "audio/ask_question_again.mp3")
		except sr.RequestError as e: 
			speech = -1
			print("Request Error.")
			system("mpg321 " + directory + "audio/offline.mp3")
	return speech

def answer(speech, lang):
	f = open(directory + "speech.txt")
	mytext = -1
	flg, cnt = 0, 0
	for text in f:
		cnt += 1
		if flg:
			f.close()
			print(text)
			cnt = cnt//3 + 1
			system("mpg321 " + directory + "audio/off_" + str(cnt) + ".mp3")
			return ""
		if text == speech + '\n':
			flg = 1
	f.close()
	mytext = web_search(speech)
	if mytext == "dont_know":
		'''mytext = "i don't know the answer yet. i will try to know the answer."
		speak(mytext, 'mb-us2')'''
		system("mpg321 " + directory + "audio/dont_know.mp3")
		mytext = ""	
	elif mytext == "offline":
		'''mytext = "i am offline. i am trying to reconnect for you."
		speak(mytext, 'mb-us2')'''
		system("mpg321 " + directory + "audio/offline.mp3")
		mytext = ""
	return mytext
	
def speak(speech, lang):
	'''speech = "'" + speech + "'"
	system("espeak -a 200 -g 5 -s 112 -v " + lang + " " + speech)'''
	try:
		myobj = gTTS(text=speech, lang=lang, slow=False) 
		myobj.save("audio/answer.mp3") 
		system("mpg321 audio/answer.mp3")
		system("rm audio/answer.mp3")	
	except sr.RequestError:
		system("mpg321 audio/offline.mp3")
	except sr.UnknownValueError:
		print("can't recognize your voice.")
	
def web_search(speech):
	#url = "http://api.wolframalpha.com/v2/query?input=" + speech + "&appid=KH88AY-V8X4LEXJV7&fbclid=IwAR0_L9b99_o4QT1lFc35E4vVMCXqLYsKK0SZ2EQA4p8lX68W8VduWcw0mhY&podindex=2"
	url = "https://app.zenserp.com/api/v2/search?apikey=3006e4b0-5578-11ea-8b01-070206ede933&q=" + speech
	try:
		'''xml = req.get(url)
		root = ET.fromstring(xml.content)
		for child in root.iter('plaintext'):
			print(child.text)
			return child.text'''
			
		ret = req.get(url)
		json_data = json.loads(ret.text)
		print(json_data)
		
		res = json_data["organic"]
		#print(len(res))
		
		if json_data["number_of_results"] == None:
			return "dont_know"
		
		min_len = min(10, len(res))
		for i in range(min_len):
			if "title" not in res[i]:
				continue
			title = res[i]["title"]
			title_parts = [x for x in title.split()]
			if 'Wikipedia' in title_parts:
				#print(res[i]["description"])
				wiki = wikipediaapi.Wikipedia('en')
				
				wiki_title = title.split(' - ')[0]
				print(wiki_title)
				wiki_res = wiki.page(wiki_title)
				
				wiki_len = min(300, len(wiki_res.summary))
				print("Page - Summary: %s" % wiki_res.summary[0:wiki_len])
				return wiki_res.summary[0 : wiki_len]
		
		for i in range(min_len):
			if "title" not in res[i]:
				continue
			return res[i]["description"]
			
		return "dont_know"
		
	except:
		return "dont_know"

	
def FACE_RECOGNITION():
	with open(directory + 'image/dataset_faces.dat', 'rb') as f:
		all_face_encodings = pickle.load(f)
	
	face_names = list(all_face_encodings.keys())
	face_encodings = np.array(list(all_face_encodings.values()))
	
	unknown_image = face_recognition.load_image_file(directory + "image/unknown.jpg")
	unknown_face = face_recognition.face_encodings(unknown_image, num_jitters = 1)
	try:
		result = face_recognition.compare_faces(face_encodings, unknown_face, tolerance = 0.5)
	except:
		'''mytext = "i coudn't recognize your face."
		speak(mytext, 'mb-us2')'''
		system("mpg321 audio/couldnt_recognize_face.mp3")
		return "visitor"
	for i in range(len(result)):
		if result[i] == True:
			return face_names[i]
	return "visitor"
	
def capture_image(image_name):
	try:
		camera            = PiCamera()
		camera.rotation   = 180
		camera.brightness = 85
		camera.contrast   = 85
		camera.sharpness  = 50
		camera.start_preview()
		sleep(1)
		camera.capture(directory + "image/" + image_name + ".jpg", resize=(480, 360))
		camera.stop_preview()
		camera.close()
	except:
		print("Camera resources locking problem. please reboot the robot.")
		system("sudo reboot")
	return 0

def museum_visit():
	#system("feh -qrYzFD2 --on-last-slide=quit --auto-zoom fill " + directory + "museum_image/")
	system("omxplayer " + directory + "video/museum_visit.mp4")	
		
def lighting(pin, state):
	if state == "ON":
		GPIO.output(pin, GPIO.HIGH)
	else:
		GPIO.output(pin, GPIO.LOW)

def mujib_speech():
	system("omxplayer " + directory + "video/mujib_speech.mp4")

def full_mujib_speech():
	system("omxplayer " + directory + "video/mujib_speech_full.mp4")

def recite_poem():
	system("omxplayer " + directory + "video/poem.mp4")

def museum_exhibition():
	system("omxplayer " + directory + "video/museum_exhibition.mp4")

def full_museum_exhibition():
	system("omxplayer " + directory + "video/museum_exhibition_full.mp4")

def museum_documentary():
	system("omxplayer " + directory + "video/museum_documentary.mp4")

def full_museum_documentary():
	system("omxplayer " + directory + "video/museum_documentary_full.mp4")

def sing_song():
	system("omxplayer " + directory + "video/song.mp3")

def sing_full_song():
	system("omxplayer " + directory + "video/song_full.mp3")
	
def main():
	system("pcmanfm --set-wallpaper='" + directory + "image/bg.jpg'")
	flg = 0
	st = time() 
	et = time()
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
			st = time()
			et = time()
			lighting(pin, "ON")	
			
			capture_image("unknown")
			
			name = FACE_RECOGNITION()
			if name != "visitor":
				print(name)
				system("pcmanfm --set-wallpaper='" + directory + "image/" + name + ".jpg'")
				name = [x for x in name.split('_')]
				name.pop()
				name = '_'.join(name)
				print(name)				
			else:
				system("pcmanfm --set-wallpaper='" + directory + "image/unknown.jpg'")
				print(name)
				
			'''mytext = "Hi "
			mytext += name
			mytext += ", how can i help you?"
			speak(mytext, "mb-us2")'''
			
			system("mpg321 " + directory + "audio/salam.mp3")
			system("mpg321 " + directory + "audio/" + name + ".mp3")
			system("mpg321 " + directory + "audio/welcome_nmst.mp3")
			system("mpg321 " + directory + "audio/how_can_i_help.mp3")
	
			
			system("rm " + directory + "image/unknown.jpg")
			lighting(pin, "OFF")
			
			speech = speech_recognition('en-us')
			
			st = time()
		
		if speech == "thank you":
			flg = 0
			st = time()
			et = time()
			system("pcmanfm --set-wallpaper='" + directory + "image/" + name + ".jpg'")

		if flg and speech != keyword:
			et = time()
			if et - st > 30:
				print(et-st, "secs without any question")
				flg = 0
				st = time()
				et = time()
				system("pcmanfm --set-wallpaper='" + directory + "image/bg.jpg'")
				continue
				
			lighting(pin, "ON")
			
			if speech == -1:
				'''mytext = "may you please ask the question again?"
				speak(mytext, 'mb-us2')'''
				continue
			elif speech in ["Museum visit", "museum visit", "visit museum", "visit Museum", "visit nmst", "visit national Museum", "visit national museum", "visit national Museum of science and technology"]:
				museum_visit()
				st = time()
			elif speech in ["speech of bangabandhu", "speech of bongobondhu", "speech of bangobandhu", "speech of bangobondhu", "speech of bongobandhu"]:
				mujib_speech()
				st = time()
			elif speech in ["full speech of bangabandhu", "full speech of bongobondhu", "full speech of bangobandhu", "full speech of bangobondhu", "full speech of bongobandhu"]:
				full_mujib_speech()
				st = time()				
			elif speech in ["who creates you", "who created you", "who made you", "who makes you"]:
				system("mpg321 " + directory + "audio/off_5.mp3")
				system("omxplayer " + directory + "video/maker.mp4")
				st = time()
			elif speech in ["recite a poem", "recite poem", "recite"]:
				recite_poem()
				st = time()		
			elif speech in ["sing a song", "play a song"]:
				sing_song()
				st = time()
			elif speech in ["sing a full song", "play a full song"]:
				sing_full_song()
				st = time()
			elif speech in ["museum exihibition", "Museum exhibition"]:
				museum_exhibition()
				st = time()
			elif speech in ["full museum exihibition", "full Museum exhibition"]:
				full_museum_exhibition()
				st = time()
			elif speech in ["museum documentary", "Museum documentary"]:
				museum_documentary()
				st = time()
			elif speech in ["full museum documentary", "full Museum documentary"]:
				full_museum_documentary()
				st = time()
			else:
				mytext = answer(speech, 'en')
				#print(mytext)
				if mytext != "":
					#speak(mytext, 'mb-us2')
					speak(mytext, 'en')
				st = time()	
			
			lighting(pin, "OFF")
		
		et = time()
		if et - st > 30:
			print(et-st, "secs without any question")
			flg = 0
			st = et = 0.00
			system("pcmanfm --set-wallpaper='" + directory + "image/bg.jpg'")

main()












