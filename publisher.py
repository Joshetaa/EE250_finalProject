import paho.mqtt.client as mqtt
import time
from pynput import keyboard
import speech2triggerWords as s2tW

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))


if __name__ == '__main__':
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