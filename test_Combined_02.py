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


message = ""


#===========================
#     CARD READER
#===========================

reader = SimpleMFRC522()

try:
	print("=======================")
	print("Place card on reader...")
	print("=======================")
	id, text = reader.read()
	message = text
	print("| id: " + str(id))
	print("| text: " + str(text))
	print("=======================")
finally:
	GPIO.cleanup()




#=======================
#     OLED DISPLAY
#=======================
serial = i2c(port=1, address=0x3c)

device = sh1106(serial)

with canvas(device) as draw:
	draw.rectangle(device.bounding_box, outline="white", fill="black")
	#draw.text((30, 40), "Hello World!", fill="white")
	#draw.text((30, 40), message, fill="white")
	draw.text((30, 40), str(id), fill="white")

sleep(10)

