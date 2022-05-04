from ast import Return
#from torch import R
import paho.mqtt.client as mqtt
import time
import sys
import threading

lock = threading.Lock()

sys.path.append('../../Software/Python/')
import grovepi
from grovepi import *
from grove_rgb_lcd import *

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the ultrasonic ranger topic here
    client.subscribe("jaleb/emotion") # subscribe to channel
    #client.subscribe("jaleb/triggerWords") # subscribe to channel
    client.subscribe("jaleb/color") # subscribe to channel
    
    
    client.message_callback_add("jaleb/display", displayCallback) # add custom call back 
    # client.message_callback_add("jaleb/triggerWords", triggerWordsCallback) # add custom call back
    client.message_callback_add("jaleb/color", colorCallback) # add custom call back 

    
#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

# CUSTOM CALL BACKS 
# custom callback for ultrasonic range finder 
def colorCallback(client, userdata, msg):
    color = str(msg.payload, "utf-8")
    print(color)
    
    if color == "Yellow":
        setRGB(255,255,0) # edit color 
    elif color == "Red":
        setRGB(255,0,0) # edit color 
    elif color == "Blue": 
        setRGB(0,255,0) # edit color 
    
    
    

def displayCallback(client, userdata, msg):
    new_msg = str(msg.payload, "utf-8")
    print(new_msg)
    
    with lock:
        setText(new_msg)    
    

    
if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        # print("delete this line")
        time.sleep(1)
