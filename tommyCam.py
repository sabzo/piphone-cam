#!/usr/bin/env python
from time import sleep

import RPi.GPIO as GPIO
import os
import pygame
import tweepy
#Script to take a picture and save it to disk
from subprocess import call
import datetime

# capture pic
def take_picture():
  date = datetime.datetime.now()
  timestamp = date.isoformat()
  success = call(["raspistill", "-o", timestamp + ".jpg"])
  print success
  permissions = call(["chmod", "+x", timestamp + ".jpg"]) 
  return str(timestamp) + '.jpg' 

#take_picture()

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

sound0 = pygame.mixer.Sound('Enter location of your 1st Soundfile here!')

sound0.play()
print "sound 1 playing"
buttonDown = False
onHook = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN) # on hook trigger
GPIO.setup(17, GPIO.IN) # button pressed trigger
GPIO.setup(18, GPIO.IN) # outA
GPIO.setup(23, GPIO.IN) # outB
GPIO.setup(24, GPIO.IN) # outC
GPIO.setup(25, GPIO.IN) # outD

GPIO.setup(27, GPIO.IN) # coin in 1

sound1 = pygame.mixer.Sound('Enter location of your 2nd soundfile here!')


def stopSound():
	pygame.mixer.stop()

def stopSomeSounds():
	sound0.stop()
	sound1.stop()

def playSelection(keyNum):
	if(keyNum == "5"):
          print('key released 4')
		#menu4.play()


def playKey(keyNum):
	if(keyNum == "0"):
		print('pressed 0')
	elif(keyNum == "1"):
		stopSound()
		print('pressed 1')
	elif(keyNum == "2"):
		stopSound()
		print('pressed 2')
	elif(keyNum == "3"):
		stopSound()
		print('pressed 3')
	elif(keyNum == "4"):
		stopSound()
		print('pressed 4')
	elif(keyNum == "5"):
        	stopSound()
        	sound1.play()
		photo_name = take_picture()
		print 'photo name: ' + str(photo_name) 
		# Consumer keys and access tokens, used for OAuth
		consumer_key = 'Enter your Twitter Consumer Key here!'
		consumer_secret = 'Enter your Twitter Consumer Secret Key here!'
		access_token = 'Enter your Twitter Access Token here'
		access_token_secret = ''

		# OAuth process, using the keys and tokens
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		# Creation of the actual interface, using authentication
		api = tweepy.API(auth)

		# Send the tweet with photo
		photo_path = '/home/pi/' + photo_name
		print photo_path
		t = datetime.datetime.now()
		status = 'Instant Photo from USC TommyCam!: ' + t.strftime('%Y/%m/%d %H:%M:%S')
		api.update_with_media(photo_path, status=status)
		print "sound 1 playing"
		print('pressed 5')
	elif(keyNum == "#"):
        	print('pressed #')

# Maps binary output to a button number.

def keyPress(outA, outB, outC, outD):
	if(outA == 1 and outB == 0 and outC == 0 and outD == 0):
		return "2"
	elif(outA == 0 and outB == 0 and outC == 0 and outD == 0):
		return "1"
	elif(outA == 0 and outB == 1 and outC == 0 and outD == 0):
		return "3"
	elif(outA == 1 and outB == 0 and outC == 1 and outD == 0):
		return "5"
	elif(outA == 0 and outB == 0 and outC == 1 and outD == 0):
		return "4"
	elif(outA == 0 and outB == 1 and outC == 1 and outD == 0):
		return "6"
	elif(outA == 1 and outB == 0 and outC == 0 and outD == 1):
		return "8"
	elif(outA == 0 and outB == 0 and outC == 0 and outD == 1):
		return "7"
	elif(outA == 0 and outB == 1 and outC == 0 and outD == 1):
		return "9"
	elif(outA == 1 and outB == 0 and outC == 1 and outD == 1):
		return "0"
	elif(outA == 0 and outB == 0 and outC == 1 and outD == 1):
		return "*"
	elif(outA == 0 and outB == 1 and outC == 1 and outD == 1):
		return "#"
	else:
		return "F"

while True:

	# Main loop.
    	# Trigger for input(4) goes low (false) when activated.
    	# Check to see if we are moving from being on the hook to off the hook...

	if(GPIO.input(4) == True and onHook == False):
		print("on hook")
		onHook = True # moving to on state
		stopSound() # stop all sounds
		buttonDown = False # just in case someone puts phone down while pressing button...

	elif(GPIO.input(4) == False and onHook == True):
		print("off hook")
            #play take camera prompt
            	sound0.play(loops=999)
		onHook = False

	elif(onHook == False):

        	# If phone is picked up, handle button presses

		if(GPIO.input(17) == True and buttonDown == False):

        		# Button pressed.
            		# To test, print out formatted binary from 74C922 chip.

			currentKey = keyPress(GPIO.input(18), GPIO.input(23), GPIO.input(24), GPIO.input(25))
			playKey(currentKey)
			buttonDown = True
#			print str(GPIO.input(18)) + " " + str(GPIO.input(23)) + " " + str(GPIO.input(24)) + " " + str(GPIO.input(25))
			print "button pressed: " + currentKey

	        # otherwise, if button released, print that and set state.
        	# if neither of these is true, the handle is up and no buttons are pressed, so do nothing.


		elif(GPIO.input(17) == False and buttonDown == True):

			# Button released - stop all DTMF sounds, reset buttonDown

			stopSound()
			currentKey = keyPress(GPIO.input(18), GPIO.input(23), GPIO.input(24), GPIO.input(25))
			playSelection(currentKey)
			print("button released: " + currentKey)
			buttonDown = False

		elif(pygame.mixer.get_busy() == False):

			sound0.play()
    	# Sleep for 100 ms then repeat.

	# print keyPress(GPIO.input(18), GPIO.input(23), GPIO.input(24), GPIO.input(25))
	# print str(GPIO.input(18)) + " " + str(GPIO.input(23)) + " " + str(GPIO.input(24)) + " " + str(GPIO.input(25))
	sleep(0.025);
