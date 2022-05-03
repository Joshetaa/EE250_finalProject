## Speech Recognition imports
import pandas as pd
import speech_recognition as sr
import sys

# facial detection imports
import tensorflow as tf
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

# MQTT Imports
import paho.mqtt.client as mqtt
import time
from pynput import keyboard
#import speech2triggerWords as s2tW

##Run facial detection
def emotionDetector(img_path)
    #load model
    temp_model = tf.keras.models.load_model('Signal Process/Emotion Recognition/Final_model_3em1.h5') 

    #load image
    face = cv2.imread(img_path)

    #load face detection file
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY) # convert image to gray scale
    faces = faceCascade.detectMultiScale(gray, 1.1, 4) 

    # Find faces in image 
    # Add boxes around each face
    for x,y,w,h in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = face[y:y+h, x:x+w]
        cv2.rectangle(face, (x, y), (x+w, y+h), (255, 0, 0), 2)
        faces2 = faceCascade.detectMultiScale(roi_gray)
        if len(faces2) == 0:
            print("Face not detected")
        else:
            for (ex, ey, ew, eh) in faces2:
                face_roi = roi_color[ey: ey+eh, ex:ex+ew]

    # Resize imgae
    final_image = cv2.resize(face_roi, (224,224))
    final_image = np.expand_dims(final_image, axis = 0)
    final_image = final_image/255.0

    # PREDICT
    Predictions = temp_model.predict(final_image) #Apply model to detemine emotion
    if (np.argmax(Predictions) == 0):
        emotion = "Anger" 
    elif (np.argmax(Predictions) == 1):
        emotion = "Hapy"
    elif( np.argmax(Predictions) == 2):
        emotion = "Sad"

    return emotion;

##Run audio detection and find trigger words
def audioDetection(audio_path, emotion)
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Audio file as source
    # listening the audio file and store in audio_text variable
    with sr.AudioFile('Audio_data/test_happy.wav') as source:
    
        audio_text = r.listen(source)
    
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
        
            # using google speech recognition
            text = r.recognize_google(audio_text)
            print('\nConverting audio transcripts into text ...')
            print(text)
     
        except:
             print('Sorry.. run again...')
    
    ## PROCESS TEXT INTO APPROPRIATE STRUCTURE (LIST OF WORDS)
    text_list = text.split()
    print("\nSplit text is: ", text_list)

    return text_list

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))


if __name__ == '__main__':
    
    emotion = emotionDetector(sys.argv[1])

    text_list = audioDetection(sys.argv[2])
    
    ## FINDING TRIGGER WORDS
    # Get dataset 
    filepath = "NRC_data/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
    emolex_df = pd.read_csv(filepath,  names=["word", "emotion", "association"], skiprows=45, sep='\t', keep_default_na=False)
    emolex_words = emolex_df.pivot(index='word', columns='emotion', values='association').reset_index()

    # inits
    sadness_words = emolex_words[emolex_words.sadness == 1].word.values
    anger_words = emolex_words[emolex_words.anger == 1].word.values
    joy_words = emolex_words[emolex_words.joy == 1].word.values
    triggerWords = []

    # get wordbase
    # emotion = sys.argv[1] # out put form caleb's script 
    if emotion == "Anger":
        word_base = anger_words
        color = "Red"
    elif emotion == "Sad":
        word_base = sadness_words
        color = "Blue"
    elif emotion == "Happy":
        word_base = joy_words
        color = "Yellow"

    # check sentence
    for word in text_list:
        if word in word_base:
            triggerWords.append(str(word))

    print("\nTrigger words for {}: ".format(emotion), triggerWords)

    # SET VARIABLES TO BE USED BY PUBLISHER 
    # emotion_string = emotion
    # triggerWords_string = ' '.join(triggerWords)
    color_string = color
    display_string = emotion + '\n'+ ''.join(triggerWords)

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    client.publish("jaleb/display", s2tW.display_string)
    # client.publish("jaleb/triggerWords", s2tW.triggerWords_string)
    client.publish("jaleb/color", s2tW.color_string)

    while True:
        # print("delete this line")
        time.sleep(1)
