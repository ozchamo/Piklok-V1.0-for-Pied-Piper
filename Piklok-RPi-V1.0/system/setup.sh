#!/bin/bash
#This file needs to be run as SUDO

#Setup local keyboard to US so I can get some work done
mv /etc/default/keyboard /etc/default/keyboard.orig
cat /etc/default/keyboard.orig | sed -e "/gb/ s/gb/us/" > /etc/default/keyboard
#Set vi as the default editor,useful for crontab -e
echo "EDITOR=vi;export EDITOR" >> ~/.profile

#Enable SSH remote access
mv /etc/rc.local /etc/rc.local.orig
cat /etc/rc.local.orig | sed -e "/exit 0/ s+exit 0+/etc/init.d/ssh start;exit 0+" > /etc/rc.local
chmod 755 /etc/rc.local

#Setup Wireless network to mine for now :(
cat<<NETWORK>>/etc/wpa_supplicant/wpa_supplicant.conf
network={
	ssid="pichus"
	psk="pichuwireless"
}
NETWORK

#TIMEZONE INFORMATION, Australia/Sydney by default for now
ln -s /usr/share/zoneinfo/Australia/Sydney /etc/localtime
echo "Australia/Sydney" > /etc/timezone

#SET UP NTP
echo y | apt-get install ntp

#NTP UPDATE THE TIME ON LOGIN:
cat <<NTPUPDATE>> ~/.profile
sudo /etc/init.d/ntp stop
sudo ntpd -qg
sudo /etc/init.d/ntp start
NTPUPDATE

#IMPROVE SOUND OUTPUT??
#I'M USING OMXPLAYER - GREAT!
#https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=13644
echo audio_pwm_mode=2 >> /boot/config.txt


#INSTALL THE BLUE BUTTON READ TIME AS A SERVICE
cat <<KLOK>>/lib/systemd/system/piklok-button-press.service

[Unit]
Description=PIKLOK BUTTON PRESS: Actions for Red and Blue buttons when pressed
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python /home/pi/Desktop/PIKLOK/bin/piklok-button-press-service.py
Restart=on-abort

[Install]
WantedBy=multi-user.target

KLOK

#and the below activates the service:
chmod +x /home/pi/Desktop/PIKLOK/bin/piklok-button-press-service.py
sudo systemctl daemon-reload
sudo systemctl enable piklok-button-press.service
sudo systemctl start piklok-button-press.service


#INSTALL THE INSTANT MESSAGE SERVICE
cat <<KLOK>>/lib/systemd/system/piklok-instant-message.service

[Unit]
Description=PIKLOK INSTANT MESSAGE: Retrieve messages posted via REDIS
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python /home/pi/Desktop/PIKLOK/bin/piklok-instant-message-service.py
Restart=on-abort

[Install]
WantedBy=multi-user.target

KLOK

#and the below activates the service:
chmod +x /home/pi/Desktop/PIKLOK/bin/piklok-instant-message-service.py
sudo systemctl daemon-reload
sudo systemctl enable piklok-instant-message.service
sudo systemctl start piklok-instant-message.service

#install the REDIS client for Python RPi
sudo pip install redis
sudo pip install python-redis

#and... load crontab for python
sudo pip install python-crontab

#ADD DEFAULT CRON JOBS
crontab -l > /tmp/picrontab
echo "* * * * * /home/pi/Desktop/PIKLOK/bin/updatepikloksettings.py # redis update of PIKLOK settings" >> /tmp/picrontab
echo "* * * * * /home/pi/Desktop/PIKLOK/bin/readtime.py # klokreadtimesettings" >> /tmp/picrontab
crontab /tmp/picrontab
rm /tmp/picrontab

#this to enable access to AWS POLLY for speach
sudo pip install boto3