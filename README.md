# EE250_finalProject

Project title: R-Emote <endl>
Project description: Social Queue Detector
Records user audio
Snaps picture of listener’s face
Sends picture and audio file to the node to be processed on VM
Facial emotion recognition
Speech to text
Search for common words
Send to Raspberry Pi to display data on RGB LCD
Emotion (text and color)
Trigger word(s)

Team Member: Caleb Flenoury, Josheta Srinivasan

Instructions: Set up your RPi but connecting an LCD screen and running the rpi_subscriber.py file in order to subscribe to the MQTT
topics proivded by the all_in_one.py file.
Next record the audio of yourself talking to someone else about that other person. You can say anything that is relating to that
person. Try to use words that will evoke a certain emotion in the person. Make sure to convert your audio to a .wav file type.
Then take a picture of this person's face once 
you are done talking. Run the all_in_one.py file with the first argument being a path to the picture file and the second argument
being a path to the audio file. 
The file should then process the input data and publish the emotion and trigger words to the MQTT
server. The RPi which has subscribed to the data from the publisher should display the information on its LCD screen. 
  
If you would like to use existing samples of videos and pictures follow the following instructions: 
  1. Sad : run 
     python3 all_in_one.py "Test files/Sadman.jpg" "Test files/Sad talk.wav"
  2. Happy : run
     python3 all_in_one.py "Test files/Happyman.jpg" "Test files/Happy talk.wav"
  3. Angry : run 
     python3 all_in_one.py "Test files/Angrywoman.jpg" "Test files/Angry talk.wav"
  

Libraries used:
- tensorflow
- pandas
- speech recognition
- open cv
- numpy
 
 Link to Demontration of the working device: https://drive.google.com/file/d/1Leg0VBkIENpzQR_ah1AMU2hyDJRl4wO4/view?usp=sharing
