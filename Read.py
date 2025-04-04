#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
	print("=======================")
	print("Place card on reader...")
	print("=======================")
	id, text = reader.read()
	print("| id: " + str(id))
	print("| text: " + str(text))
	print("=======================")
finally:
	GPIO.cleanup()

