from os import system
#import face_recognition
from gtts import gTTS 
import pickle
import numpy as np 
import RPi.GPIO as GPIO
import speech_recognition    as sr
from time import sleep
from picamera import PiCamera
from googletrans import Translator

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
			#speech = bangla_translation()
		except sr.UnknownValueError: 
			speech = -1
			print("Nick could not understand audio")  
		except sr.RequestError as e: 
			speech = -1
			print("Request Error.")
	return speech

def translation(speech, lang):	
	translator = Translator()
	speech = (translator.translate(speech, dest = lang)).text
	return speech

speech = "Sorry, I am offline" #speech_recognition("bn-BD")
speech = translation(speech, "bn")
print(speech)













