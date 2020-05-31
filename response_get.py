from serial import Serial  
from os import system

port = '/dev/ttyACM0'
baudrate = 9600
ser = Serial(port, baudrate)

while True: 
	if(ser.inWaiting() >0):
		line = ser.readline()
		line = line.decode('utf-8')
		print(line)
		if line == 'walle record audio\r\n':
			system('python3 /home/pi/Desktop/OfficeAssistantRobot/audio_record.py')
		elif line == 'walle play audio\r\n':
			system('python3 /home/pi/Desktop/OfficeAssistantRobot/audio_play.py')
		elif line == 'walle open document\r\n':
			system('python3 /home/pi/Desktop/OfficeAssistantRobot/document_open.py')
		elif line == 'fire detected\r\n':
			system('python3 /home/pi/Desktop/OfficeAssistantRobot/fire_alarm.py')
		elif line == 'weather\r\n':
			system('python3 /home/pi/Desktop/OfficeAssistantRobot/weather_forecast.py')
		elif line == 'reached\r\n':
			system('python3 /home/pi/Desktop/OfficeAssistantRobot/destination_message.py')
		system('python3 /home/pi/Desktop/OfficeAssistantRobot/response_post.py')
			
