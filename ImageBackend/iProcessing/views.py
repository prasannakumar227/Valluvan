from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

import pytesseract
import shutil
import os
import random
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.image

from langdetect import detect
import os
import gtts as gt
from translate import Translator
from textblob import TextBlob
from translate import Translator
from IPython.display import Audio, display
from pathlib import Path
from .models import image
from .views import render
from langcodes import *
from googletrans import Translator, constants
from pprint import pprint
import googletrans
import translators as ts
import translators.server as tss

BASE_DIR = Path(__file__).resolve().parent.parent

#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def imageFunction(imagefile):
   # -*- coding: utf-8 -*-
# original image
   ori_image = cv2.imread("POSTFiles/images/"+str(imagefile))
   print(type(str(imagefile)))

   ori_img = cv2.cvtColor(ori_image, cv2.COLOR_BGR2RGB)
   # plt.imshow(ori_img)
   # plt.axis('off')
   # plt.show()

   fixed_img = cv2.resize(ori_img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
   # plt.imshow(fixed_img)
   # plt.axis("off")

   ogimg = cv2.cvtColor(fixed_img, cv2.COLOR_RGB2GRAY)

   kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
   dilation = cv2.dilate(ogimg, kernel, iterations=1)
   # plt.imshow(dilation)
   # plt.axis("off")

   kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
   erosion= cv2.erode(dilation, kernel, iterations=1)
   # plt.imshow(erosion)
   # plt.axis("off")

   binary = cv2.threshold(cv2.medianBlur(erosion, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
   # plt.imshow(binary)
   # plt.axis("off")

   gsbin = binary.astype(np.uint8)
   # gsbin= 255 * gsbin
   # plt.imshow(gsbin)

   image2 = cv2.cvtColor(255-gsbin, cv2.COLOR_GRAY2RGB)
   # plt.imshow(image2)
   # plt.axis('off')
   # plt.show()
   # kernel = np.array([[-1, -1, -1],
   #                 [-1, 5,-1],
   #                 [-1, -1, -1]])
   # final_img = cv2.filter2D(src=image2, ddepth=-1, kernel=kernel)

   matplotlib.image.imsave('image1.png', image2)

   extractedText = pytesseract.image_to_string("image1.png",lang='eng+hin+kan+tel+mal',config='--psm 6')
   extractedText= extractedText.replace('\n', ' ')

   print(extractedText+"\n")

   lang = detect(extractedText)
   print(lang+"\n")


   lang3=Language.get(lang).to_alpha3()
   print(lang3)

   # extractedText = pytesseract.image_to_string("image1.png",lang=lang3,config='--psm 6')
   # extractedText= extractedText.replace('\n', ' ')

   translation = tss.google(extractedText, from_language=lang, to_language='en-US')

   # translator= Translator(from_lang=lang,to_lang="en")
   # translation = translator.translate(extractedText)
   print(translation+"\n")

   trans = ""
   i=0
   preele= ""
   for element in translation:
      i+=1
      n = ord(element)
      if 97 <= n <= 122 or 65<=n<=90 or 48<=n<=57:
            trans=trans+element
      else:
            if(preele==" "):
               trans=trans+""
            else:
               trans=trans+" "
      preele=element
      #print(element, end=' ')
      if(i==499):
            break;
   print(trans)

   trans1 = ""
   i=0
   preele= ""
   for element in trans:
      i+=1
      n = ord(element)
      if 97 <= n <= 122 or 65<=n<=90 or 48<=n<=57:
            trans1=trans1+element
      else:
            if(preele==" "):
               trans1=trans1+""
            else:
               trans1=trans1+" "
      preele=element
      #print(element, end=' ')
      if(i==499):
            break;
   print(trans1+"\n")


   tb_txt = TextBlob(trans1)

   correctedTBText = tb_txt.correct()
   correctedText = str(correctedTBText)

   print("Corrected Text:"+str(correctedText)+"\n")


   # translator= Translator(from_lang="en",to_lang="ta")
   # translation = translator.translate(trans1)
   # print(translation+"\n")
   translation = tss.google(correctedText, from_language='en-US', to_language='ta')

   print(translation+"\n")

   txt=translation
   tts=gt.gTTS(text=txt,lang="ta")
   tts.save("POSTFiles/audio/ttso.wav")
   #os.system("ttso.wav")


   sound_file = 'ImageBackend/POSTFiles/audio/ttso.wav'
   display(Audio(sound_file, autoplay=True))


@api_view(['GET','POST'])
def imageProcessing(request):
   if request.method=='POST':
      imagefile = request.FILES["picture"]
      postimage = image(
         img = imagefile
        )
      postimage.save()  
      imagefile = "toProcessImage.jpg"
      finalimg = os.path.join(BASE_DIR,'POSTimages/images/') + str(imagefile) 
      #imgProcess
      print((imagefile))
      print(type(imagefile))
      print(finalimg)
      imageFunction(imagefile)
      Data = os.path.join(BASE_DIR,'POSTFiles/audio/abc3.wav')
      print("AUDIO File successfully sent: "+ Data)
      context = {
         'audioready':True,
         'link': '/ImageBackend/POSTFiles/audio/ttso.wav',

      }
      postimage.delete()
      path = "/Users/prasannakumar/Documents/Thirukkural_Size'_a_Code/TamilHack'/ImageBackend/POSTFiles/images/toProcessImage.jpg"
      if os.path.isfile(path):
         os.remove(path)

      return render(request, "iProcessing/index.html",context)
   return render(request, "iProcessing/index.html")
