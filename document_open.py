from serial import Serial  
from os import system

port = '/dev/ttyACM0'
baudrate = 9600
ser = Serial(port, baudrate)

i = True

system("espeak -s 10 'Wallie wants to know the password.'")
system('python3 /home/pi/Desktop/OfficeAssistantRobot/response_post.py')

while i: 
	if(ser.inWaiting() >0):
		line = ser.readline()
		line = line.decode('utf-8')
		print(line)
		if line == 'open box\r\n':
			system("espeak -s 10 'yahoooo. password matched.'")
			system("espeak -s 10 'wallie is opening heart for you.'")
			system('python3 /home/pi/Desktop/OfficeAssistantRobot/response_post.py')
			while i:
				if(ser.inWaiting() >0):
					line1 = ser.readline()
					line1 = line1.decode('utf-8')
					print(line1)
					if line1 == 'close box\r\n':
						system("espeak -s 10 'wallie has taken your document in his heart.'")
						i = False
		else:
			system("espeak -s 10 'haha. Wrong password? Wallie is intelligent.'")
			system("espeak -s 10 'you can not full wallie.'") # full -> fool
			i = False
		system('python3 /home/pi/Desktop/OfficeAssistantRobot/response_post.py')
					
