#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import sys
import os.path

sys.path.insert(0,"/home/pi/Desktop/PIKLOK/bin")
from playaudio import play_audio_file
from speakmessage import speak_text_message_from_redis,delete_spoken_text_from_redis

time.sleep(5)

while 1:

	with open('/home/pi/Desktop/PIKLOK/bin/RED-BUTTON-SERVICE-DEFINITION', 'r') as content_file:
 		redbuttonmode = content_file.read()

	if redbuttonmode == "read-message-now-stop" or redbuttonmode == "":
	
		print "calling on redis"
		redisresult=speak_text_message_from_redis("messagetospeak")

		if redisresult == 0:
			time.sleep(15)
		else:
			while 1:
				if os.path.exists("/home/pi/Desktop/PIKLOK/bin/messagetospeakfile.mp3") == True:
					play_audio_file("/home/pi/Desktop/PIKLOK/bin/messagetospeakfile.mp3")
					time.sleep(2)
				else:
					break
	else:
		# We cool this service down for now as it's not active!
		time.sleep(60)
