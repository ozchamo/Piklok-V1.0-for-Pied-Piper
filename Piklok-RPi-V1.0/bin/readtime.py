#!/usr/bin/python
#import pyaudio
#import wave
import time
import sys
from subprocess import call
sys.path.insert(0,"/home/pi/Desktop/PIKLOK/bin")
from playaudio import play_audio_file

def readtime():
	
	sounds="/home/pi/Desktop/PIKLOK/sounds/"

	def play_audio_wav_omxplayer(audiofile):
		call(["/usr/bin/omxplayer",audiofile])
	
	if len(sys.argv) == 1:
		#READ OUT THE CURRENT TIME
		print("No arguments passed - reading the current time. For tests, pass HH MM as parameters, where HH is 0-23")
	
		timeisnow=time.localtime()
		#positional arguments are:
		#time.struct_time(tm_year=2017, tm_mon=8, tm_mday=24, tm_hour=22, tm_min=3, tm_sec=30, tm_wday=3, tm_yday=236, tm_isdst=0)
	
		tm_year=timeisnow[0]
		tm_mon=timeisnow[1]
		tm_day=timeisnow[2]
		tm_hour=timeisnow[3]
		tm_min=timeisnow[4]
		tm_sec=timeisnow[5]
		tm_weekday=timeisnow[6]
	
		str_tm_year=str(tm_year)
		str_tm_mon=str(tm_mon)
		str_tm_day=str(tm_day)
		str_tm_sec=str(tm_sec)
	
	else:  
		#DUMMY RUN - READ OUT THE HH and MM passed as arguments
		if len(sys.argv) == 3:
			tm_hour=int(sys.argv[1])
			tm_min=int(sys.argv[2])
			print("TEST READ: " + sys.argv[1] +":"+ sys.argv[2])
		else:
			print("For testing you need to pass 3 arguments, HH MM AM/PM, where HH is a number between 0 and 23.")
			exit()
	
	amorpm="am"
	if tm_hour == 0:
		tm_hour=12
		amorpm="am"
	if tm_hour == 12:
		amorpm="pm"
	if tm_hour > 12:
		tm_hour=tm_hour-12
		amorpm="pm"
	
	str_tm_hour=str(tm_hour)
	str_tm_hour_next=str(tm_hour+1)
	str_tm_min=str(tm_min)
	
	#basic or advanced - this for fun to speak the time in more sophisticated ways
	#timetoread is the variable that holds the output to read
	MODE="basic" 
	
	if MODE == "basic":
	
		openingphrase="thetimeisnow "
		done=0
	
		if tm_min == 0:  # it's an "o'clock"
			if amorpm == "am":
				hourphrase=str_tm_hour + " oclock inthemorning"
			if amorpm == "pm":
				if tm_hour > 0 and tm_hour < 6:	
					hourphrase=str_tm_hour + " oclock intheafternoon"
					print("hourphease is "+ hourphrase)
				if tm_hour > 5 and tm_hour < 9:	
					hourphrase=str_tm_hour + " oclock intheevening"
				if tm_hour > 8: 
					hourphrase=str_tm_hour + " pm"
		else:
			if tm_min < 10:
				hourphrase=str_tm_hour + " 0 " + str_tm_min + " " + amorpm
			else:
				hourphrase=str_tm_hour + " " + str_tm_min + " " + amorpm
	
		timetoread=openingphrase + " " + hourphrase
	
	
	if MODE == "advanced":
	
		openingphrase="thetimeisnow "
		done=0
	
		if tm_min == 0:  # it's an "o'clock"
			hourphrase=str_tm_hour+" oclock"
			done=1
	
		if tm_min == 5:
			hourphrase="5 past " + str_tm_hour 
			done=1
	
		if tm_min == 10:
			hourphrase="10 past " + str_tm_hour
			done=1
	
		if tm_min == 15:
			hourphrase="aquarterpast " + str_tm_hour
			done=1
		
		if tm_min == 20:
			hourphrase="20 past " + str_tm_hour
			done=1
		
		if tm_min == 25:
			hourphrase="25 past " + str_tm_hour
			done=1
		
		if tm_min == 30:
			hourphrase="half past " + str_tm_hour
			done=1
	
		if tm_min == 35:
			hourphrase="25 to " + str_tm_hour_next
			done=1
	
		if tm_min == 40:
			hourphrase="20 to " + str_tm_hour_next
			done=1
	
		if tm_min == 45:
			hourphrase="aquarterto " + str_tm_hour_next
			done=1
	
		if tm_min == 50:  
			hourphrase="10 to " + str_tm_hour_next
			done=1
	
		if tm_min == 55:  # past the hour
			hourphrase="5 to " + str_tm_hour_next
			done=1
	
		if done == 0:
			if tm_min < 10:
				hourphrase=str_tm_hour + " 0 " + str_tm_min
			else:
				hourphrase=str_tm_hour + " " + str_tm_min 
	
		timetoread=openingphrase+" "+hourphrase+" "+amorpm
	
	for word in str.split(timetoread):
		play_audio_file(word)
	       



def main():
	readtime()

if __name__=="__main__":
	main()

