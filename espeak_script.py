from gtts import gTTS
import os
tts = gTTS(text='shah alom, how are you?', lang='en',slow=False)
tts.save("test.mp3")
os.system("mpg321 test.mp3")
