#!/usr/bin/env python

#--------------------
# CARD READER IMPORTS
#--------------------
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


#--------------------
# OLED SCREEN IMPORTS
#--------------------
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, sh1107, ws0010
from time import sleep

#--------------------
# NETWORK IMPORTS
#--------------------
import socket




# setup network connection
#--------------------------
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.11', 50000)) # game server





message = ""

while(1):	#loop forever


	#===========================
	#     CARD READER
	#===========================

	reader = SimpleMFRC522()

	try:
		print("=======================")
		print("Place card on reader...")
		print("=======================")
		id, text = reader.read()			# waits here until RFID tag read
		message = text
		print("| id: " + str(id))
		print("| text: " + str(text))
		print("=======================")
	finally:
		GPIO.cleanup()

	#=======================
	#    NETWORK SEND
	#=======================
	client_socket.sendall(str(id).encode())		# sends RFID tag id to game server


	#=======================
	#     OLED DISPLAY
	#=======================
	serial = i2c(port=1, address=0x3c)

	device = sh1106(serial)

	with canvas(device) as draw:
		draw.rectangle(device.bounding_box, outline="white", fill="black")
		#draw.text((30, 40), "Hello World!", fill="white")
		#draw.text((30, 40), message, fill="white")
		draw.text((30, 40), str(id), fill="white")					# display tag ID on screen

	sleep(3)


client_socket.close()
