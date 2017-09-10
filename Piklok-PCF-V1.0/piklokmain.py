import os
import uuid
import time
import redis
import boto
import requests
import json
from flask import Flask,render_template, redirect, request, url_for, make_response

app = Flask(__name__)

piklokdb = redis.Redis(host='KEYREPLACE-YOUR-REDIS-HOST', port='10038', password='KEYREPLACE-YOUR-REDIS-PASSWORD')

with open('RPI-UUID', 'r') as content_file:
	clientid = content_file.read()
	

@app.route('/')
def mainmenu():

	ecs_user_key='KEYREPLACE-YOUR-ECS-USER-KEY'
	ecs_access_key_id = 'KEYREPLACE-YOUR-ECS-USER-KEY@ecstestdrive.emc.com'
	ecs_secret_key = 'KEYREPLACE-YOUR-ECS-SECRET-KEY'

	session = boto.connect_s3(ecs_access_key_id, ecs_secret_key, host='object.ecstestdrive.com')
	bucket = session.get_bucket('piklok')

	key = bucket.get_key("talkclock.png")
	key.set_acl('public-read')

	pikloklogo="http://" + ecs_user_key + ".public.ecstestdrive.com/" + bucket.name + "/talkclock.png"

	page="""
	<center>
	
	<IMG SRC="{}" width="150">
	<HR>

	<h2>
	PiKlok :: Magic</br>
	</h2>
	<hr>
	<h3>
	<a href="/timereadout">Time Read-Out<BR>Frequency</a></br><br>
	<a href="/talkinghours">Talking Hours</a></br><br>
	<a href="/sendspokenmessage">Send a Message<BR> to be Spoken Out</a></br>
	</h3>
	</center>
	""".format(pikloklogo)

	return render_template('piklok-render.html',page=page)

@app.route('/timereadout_post', methods=['POST'])
def timereadout_post():

	## This is how you grab the contents from the form
	readfrequency = request.form['readfrequency']
	piklokdb.hmset(clientid, {'readfrequency':readfrequency})
	resp = """
	<meta http-equiv="refresh" content="0; url=/" />
	"""

	return resp.format()


@app.route('/timereadout')
def timereadout():
	
	page= """
	    </br><center><h2>Time Read-Out Frequency</h2></center>
	    <hr>

	    <form method="post" action="/timereadout_post">

			<center>
	        <tr>
	        <td></td>
	        <td>
	        <P>Pick the time readout frequency for your klok:</P>
	        <input type="radio" name="readfrequency" value="1" checked>Every Minute<br>
	        <input type="radio" name="readfrequency" value="5" checked>Every 5 minutes<br>
	        <input type="radio" name="readfrequency" value="10" checked>Every 10 minutes<br>
	        <input type="radio" name="readfrequency" value="15" checked>Every 15 minutes<br>
	        <input type="radio" name="readfrequency" value="20" checked>Every 20 minutes<br>
	        <input type="radio" name="readfrequency" value="30" checked>Every half hour<br>
	        <input type="radio" name="readfrequency" value="60" checked>On the hour, every hour<br>

	        <BR><HR>
	            
	        <input type="submit" value="DONE"></center>

	    </form>
	    </td>
	    <td></td>
	    </tr>

	    """
	
	return render_template('piklok-render.html',page=page)



@app.route('/talkinghours')
def talkinghours():
	
	page = """
	    </br><center><h2>Talking hours - when is your klok allowed to read?</h2>
	    <hr>

	    <form method="post" action="/talkinghours_post">

	        <tr>
	        <td>

	        <BR>
	        <P>Start talking at:
	        <select name="talkstart">
				<option value="25">Always Talk</option>
				<option value="26">Never Talk</option>
		        <option value="5">05:00 AM</option>
		        <option value="6">06:00 AM</option>
		        <option value="7">07:00 AM</option>
		        <option value="8">08:00 AM</option>
		        <option value="9">09:00 AM</option>
		        <option value="10">10:00 AM</option>
		        <option value="11">11:00 AM</option>
	        </select>

	        <P>Go quiet at:
	        <select name="talkend">
				<option value="0">--------</option>
	            <option value="18">06:00 PM</option>
	            <option value="19">07:00 PM</option>
	            <option value="20">08:00 PM</option>
	            <option value="21">09:00 PM</option>
	            <option value="22">10:00 PM</option>
	            <option value="23">11:00 PM</option>
	        </select>
		<BR><BR><HR>
	         <input type="submit" value="DONE"></center>
		<BR>

	    </form>
	    </td>
	    <td></td>
	    </tr>

	"""
	
	return render_template('piklok-render.html',page=page)


@app.route('/talkinghours_post', methods=['POST'])
def talkinghours_post():

	talkstart = request.form['talkstart']
	talkend = request.form['talkend']

	if talkstart == "25":  #Always talk
		talkstart=0
		talkend=23

	if talkstart == "26":  #Never talk
		talkstart=0
		talkend=0

	piklokdb.hmset(clientid, {'talkstart':talkstart,'talkend':talkend})

	resp = """
	<meta http-equiv="refresh" content="0; url=/" />
	"""

	return resp.format()


@app.route('/sendspokenmessage')
def sendspokenmessage():
	
	wu_Key = "KEYREPLACE-YOUR-WU-KEY"
 
	url = "http://api.wunderground.com/api/" + wu_Key + "/conditions/q/au/sydney.json"
 
	res = requests.get(url)
	res_json = json.loads(res.content)
	weather = res_json["current_observation"]["weather"]
	temp = res_json["current_observation"]["temp_c"]

	page = """
	    </br><center><h2>Send a text message to be spoken on the klok:</h2>
	    <hr>

	    <form method="post" action="/sendspokenmessage_post">
			<p>Type your message below and press the 'send' button:</p>
			<input type="text" name="messagetospeak" style="width: 500px;"><br><br>
             <hr><br>

             <input type="submit" value="SEND"/>
	    </form>
		<hr><br>

		How about having the current weather spoken?<BR> Below the current weather for Sydney, courtesy of WeatherUnderground:<BR><BR>
		[ The weather in Sydney right now is {}, with a temperature of {} degrees celsius. ]

		<BR>
	    </td>
	    <td></td>
	    </tr>
	</center>

	    """.format(weather,temp)
	
	return render_template('piklok-render.html',page=page)

@app.route('/sendspokenmessage_post', methods=['POST'])
def sendspokenmessage_post():

	messagetospeak = request.form['messagetospeak']
	piklokdb.hmset(clientid, {'messagetospeak':messagetospeak})

	resp = """
    <meta http-equiv="refresh" content="0; url=/" />
    """

	return resp.format()

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
