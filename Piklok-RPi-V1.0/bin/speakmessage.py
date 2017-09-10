#!/usr/bin/python
import boto3
import sys
import redis
from playaudio import play_audio_file

#region_name='ap-southeast-2'

def get_dev_and_client_ids():

	global piklokdb
	global clientid 

	aws_access_key_id = "KEY-REPLACE-YOUR-ACCESS-KEY-ID"
	aws_secret_access_key = "KEYREPLACE-YOUR-AWS-SECRET-ACCESS-KEY"

	# Get REDIS DB

	# Get RPi id (this is in a file for now)
	with open('/home/pi/Desktop/PIKLOK/bin/RPI-UUID', 'r') as content_file:
		clientid = content_file.read()

	piklokdb = redis.Redis(host='KEYREPLACE-YOUR-REDIS-HOST', port='10038', password='KEYREPLACE-YOUR-REDIS-PASSWORD')


def speak_text_message(messagetospeak):

	get_dev_and_client_ids()

		polly = boto3.client('polly',aws_access_key_id = "KEY-REPLACE-YOUR-ACCESS-KEY-ID",aws_secret_access_key = "KEYREPLACE-YOUR-AWS-SECRET-ACCESS-KEY", region_name='us-west-2')

	response = polly.synthesize_speech(
   		OutputFormat='mp3',
   		Text=messagetospeak,
   		TextType='text',
   		VoiceId='Joanna')

	with open('/home/pi/Desktop/PIKLOK/bin/messagetospeakfile.mp3', 'wb') as messagefile:
		messagefile.write(response['AudioStream'].read())

	play_audio_file("/home/pi/Desktop/PIKLOK/bin/messagetospeakfile.mp3")
	

def get_text_message_from_redis(messageid):
	
	get_dev_and_client_ids()

	message = piklokdb.hmget(clientid,messageid)
	
	if message == [None]:
		return("")
	else:
		return(message[0])


def speak_text_message_from_redis(messageid):

	messagetospeak = get_text_message_from_redis(messageid)

	if messagetospeak == "":
		return(0)
	else:
		speak_text_message(messagetospeak)
		return(1)


def delete_spoken_text_from_redis(messageid):

	get_dev_and_client_ids()

	piklokdb.hdel(clientid,messageid)
	


def main(argv):
	if len(argv) < 2:
		print("Speaks out text passed as parameter.\n\nUsage: %s filename" % sys.argv[0])
	else:
		#speaks the string contained in the first arg unless it is "redis"
		#if first arg is "redis" then speak the message in redis if there is no
		#second arg, otherwise fetch the second arg from redis

		if argv[1] == "redis":
			if len(argv) == 3:
				redisresult=speak_text_message_from_redis(argv[2])
			else:
				redisresult=speak_text_message_from_redis("messagetospeak")
		else:
			speak_text_message(argv[1])

if __name__=="__main__":
	main(sys.argv)

