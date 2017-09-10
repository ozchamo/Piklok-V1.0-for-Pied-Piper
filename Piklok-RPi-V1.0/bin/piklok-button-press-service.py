#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import sys
import os
from subprocess import call
from speakmessage import delete_spoken_text_from_redis, speak_text_message
from playaudio import play_audio_file
sys.path.insert(0,"/home/pi/Desktop/PIKLOK/bin")
from readtime import readtime

## Let's define all the GPIO good stuff here

GPIO.setmode(GPIO.BOARD)  	# Numbers pins by physical location

# PIN 7  we use for BLUE BUTTON, to read the time
BUTTON1=7
GPIO.setup(BUTTON1, GPIO.IN)  # Set pin mode as input

# PIN 11  we use for RED BUTTON, to stop remote message repeat
BUTTON2=11
GPIO.setup(BUTTON2, GPIO.IN)  # Set pin mode as input

call(["/home/pi/Desktop/PIKLOK/bin/readIPaddress.py",""])
play_audio_file("piklok-is-operational.mp3")

while 1:

	if GPIO.input(BUTTON1) == 0:
			readtime()

	if GPIO.input(BUTTON2) == 0:

		#The "functions of the red button
		with open('/home/pi/Desktop/PIKLOK/bin/RED-BUTTON-SERVICE-DEFINITION', 'r') as content_file:
			redbuttonmode = content_file.read()
	
		if redbuttonmode == "read-message-now-stop" or redbuttonmode == "":
			# This is the default functionality
			messagetospeak="/home/pi/Desktop/PIKLOK/bin/messagetospeakfile.mp3"

			if os.path.isfile(messagetospeak):
				os.remove(messagetospeak)
				delete_spoken_text_from_redis("messagetospeak")
