import pytesseract
import os
import gtts as gt
import re
from langdetect import detect
from translate import Translator
from IPython.display import Audio, display
import easygui

try:
    from PIL import Image
except ImportError:
    import Image


def imageFunction(img):
   extractedInformation = pytesseract.image_to_string(img,lang='eng+hin+tel+kan+tam+mal')
   extractedInformation = extractedInformation.replace('\n', ' ')

   print(extractedInformation)

   lang = detect(extractedInformation)
   print(lang)
   translator= Translator(from_lang=lang,to_lang="en")
   translation = translator.translate(extractedInformation)
   print(translation)
   trans = re.sub('[^A-Za-z0-9]+,', ' ', translation)
   print(translation)
   print(trans)
   translator= Translator(from_lang="en",to_lang="ta")
   translation = translator.translate(trans)
   print(translation)
   txt=translation
   tts=gt.gTTS(text=txt,lang="ta")
   tts.save("abc3.wav")
   os.system("abc3.wav")
   sound_file = 'abc3.wav'
   display(Audio(sound_file, autoplay=True))

try:
   img = easygui.fileopenbox()
   print(img)
   imageFunction(img)
except Exception as e:
   print("Error: " + str(e))

