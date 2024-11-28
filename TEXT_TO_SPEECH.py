from gtts import gTTS
import os 
f = open("sample.txt",encoding="utf-8")
x = f.read()
print(x)
language= "ar"
audio = gTTS(text=x,slow=False)
audio.save("audio.mwv")
os.system("audio.mwv")
