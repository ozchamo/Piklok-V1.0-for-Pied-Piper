
#!/usr/bin/python
import boto3
import sys
import redis
from playaudio import play_audio_file


def get_red_button_mode()

	#The "functions of the red button
	with open('/home/pi/Desktop/PIKLOK/bin/RED-BUTTON-SERVICE-DEFINITION', 'r') as content_file:
		redbuttonmode = content_file.read()

def set_red_button_mode()

	#The "functions" of the red button:
	#  read-message-now-stop
	#  speak-the-weather
	
	


#def main(argv):
#	if len(argv) < 2:
#		print("Speaks out text passed as parameter.\n\nUsage: %s filename" % sys.argv[0])
#	else:
#		#speaks the string contained in the first arg unless it is "redis"
#		#if first arg is "redis" then speak the message in redis if there is no
#		#second arg, otherwise fetch the second arg from redis
#
#		if argv[1] == "redis":
#			if len(argv) == 3:
#				redisresult=speak_text_message_from_redis(argv[2])
#			else:
#				redisresult=speak_text_message_from_redis("messagetospeak")
#		else:
#			speak_text_message(argv[1])
#
#if __name__=="__main__":
#	main(sys.argv)
##
