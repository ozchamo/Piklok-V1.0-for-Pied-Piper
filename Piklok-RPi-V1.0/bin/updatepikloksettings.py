#!/usr/bin/python
import redis
from crontab import CronTab

piklokdb = redis.Redis(host='KEYREPLACE-YOUR-REDIS-HOST', port='10038', password='KEYREPLACE-YOUR-REDIS-PASSWORD')

with open('RPI-UUID', 'r') as content_file:
	clientid = content_file.read()

piklokcrontab=CronTab(user="pi")


### READ TIMJE FREQUENCY  AND QUITE HOURS
readfrequency=piklokdb.hmget(clientid,"readfrequency")[0]
talkstart=piklokdb.hmget(clientid,"talkstart")[0]
talkend=piklokdb.hmget(clientid,"talkend")[0]

print "UPDATING TO FREQUENCY "+readfrequency+ " START/END "+ str(talkstart) +"/"+ str(talkend)  

crontabid="klokreadtimesettings"

#First - we find the crontab line for reading the time freq 
#and put it in "readtimejob"
for readtimejob in piklokcrontab:
	if readtimejob.comment == crontabid:
		break

if talkstart == "0" and talkend == "0":
	#The klok is not supposed to talk
	#We disable the entry from the crontab altogether
	readtimejob.enable(False)
	print("The request was to disable (silence) the klok")
	piklokcrontab.write()

else:
	# FIRST, FREQUENCY OF TALKING
	# Dead easy since the time interval is a number!
	readtimejob.minute.every(readfrequency)
	
	# NOW FOR START AND END TALKING TIMES
	# these times are in talkstart and talkend

	#There may be no quiet time, talk all the time at the minutes specified above
	if talkstart == "0" and talkend == "24":
		readtimejob.hour.every(1)
	else:
		readtimejob.hour.during(talkstart,talkend)

	#And now we commit the changes!
	if readtimejob.is_valid():
		readtimejob.enable()
		piklokcrontab.write()
	else:
		print("could not update the crontab with invalid job: FREQUENCY "+readfrequency+ " START/END "+ str(talkstart) +"/"+ str(talkend))
	

## RED BUTTON SETUP

red_button_mode=piklokdb.hmget(clientid,"red_button_mode")

if red_button_mode == [None]:
		# The mode for the red button has not been defined - default is talk a message
		with open("/home/pi/Desktop/PIKLOK/bin/RED-BUTTON-SERVICE-DEFINITION", "w") as file:
			text_file.write("read-message-now-stop")


