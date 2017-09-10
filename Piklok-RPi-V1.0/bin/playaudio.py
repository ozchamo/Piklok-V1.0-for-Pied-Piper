#!/usr/bin/python
import time
import sys
import os.path
from subprocess import call

sounds="/home/pi/Desktop/PIKLOK/sounds/"
	
def play_audio_file_omxplayer(audiofile):
	#Best to not call this directly from anywhere else
	call(["/usr/bin/omxplayer",audiofile])

def play_audio_file(audiofile):
	#The idea is that omxplayer is hidden so that it can be changed later
	if os.path.splitext(audiofile)[1] == "":
		play_audio_file_omxplayer(sounds+audiofile+".wav")
	else:
		print("now here")
		if os.path.exists(audiofile) == True:
			print("now here 1")
			play_audio_file_omxplayer(audiofile)
		else:
			print("now here 2")
			if os.path.exists(sounds+audiofile) == True:
				print("now here 3")
				play_audio_file_omxplayer(sounds+audiofile)
	
def play_audio_list(audiofilelist):
	for index in range(0,len(audiofilelist)):
		play_audio_file(audiofilelist[index])
	
def main(argv):
	if len(argv) < 2:
		print("Plays a wave file (extension not required).\n\nUsage: %s filename.wav" % sys.argv[0])
	else:
		play_audio_list(argv)

if __name__=="__main__":
	main(sys.argv)

