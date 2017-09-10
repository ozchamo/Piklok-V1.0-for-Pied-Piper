#!/usr/bin/python

from subprocess import check_output
import sys
sys.path.insert(0,"/home/pi/Desktop/PIKLOK/bin")
from playaudio import play_audio_file

myipaddr=check_output(['hostname','-I'])

for digit in myipaddr:
	if digit != ' ' and digit != '\n':
		if digit == ".":
			play_audio_file("dot")
		else:
			play_audio_file(digit)

