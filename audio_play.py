import pyaudio
import wave
from os import system

system("espeak -s 10 'Wallie is a good robot. He is playing audio for you.'")

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 10 # seconds to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'audio_msg.wav' # name of .wav file

audio = pyaudio.PyAudio() # create pyaudio instantiation

wf = wave.open('/home/pi/Desktop/OfficeAssistantRobot/audio_msg.wav', 'rb') #get the file to play

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,output = True, \
                    frames_per_buffer=chunk)
frames = []

# Read data in chunks
data = wf.readframes(chunk)

# Play the sound by writing the audio data to the stream
while data != '':
    stream.write(data)
    data = wf.readframes(chunk)

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

system("espeak -s 10 'Wallie finished playing audio.'")
