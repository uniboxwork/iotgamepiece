# =====================================================================================
#  IoT Game Piece - v0.1
# =====================================================================================
""" [to be done] Registers with game server
    Receives messages from game server
    Updates state
    Checks state
    Displays on OLED screen
    Reads RFID tag location
    Transmits location to game server
"""


#--------------------
# CARD READER IMPORTS
#--------------------
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


# --------------------
# OLED SCREEN IMPORTS
# --------------------
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, sh1107, ws0010
from time import sleep

# -----------------
# NETWORK IMPORTS
# -----------------
import socket

# ---------------
# THREAD IMPORTS
# ---------------
from threading import Thread





# ---------------------------
#     OLED DISPLAY SETUP
# ---------------------------
serial = i2c(port=1, address=0x3c)
device = sh1106(serial)




# ===========
# Variables
# ===========
finished = False        # flag for execution stop

finishedRFID = False    # flag for RFID thread execution stop
finishedNetIN = False   # flag for networkIN thread execution stop
finishedNetOUT = False  # flag for networkOUT thread execution stop


currentSquare = 0       # holds most recently read square (RFID tag serial number)
previousSquare = 0      # holds previous read squire (RFID tag serial number)
messageOutBox = []      # holder for messages to be sent
separator = '#'         # seperator of fields in network messages

# message
# -----------
messageRaw = ""         # holds raw message received over network
messageFrom = ""        # separated message sender
messageSubject = ""     # separated message subject
messageContent = ""       # separated message value

#device variables
deviceName = "gp1"





# ============
# sendMessage
# ============
# adds a message to the outbox for sending
# format:      deviceName#subject#content   e.g.  gp1#TAG#8988789789
def sendMessage(subject="NO SUBJECT", content="NO VALUE"):
    #compose message and add to outBox...
    messageOutBox.append(deviceName + separator + subject + separator + content)



# LOAD UP SOME TEST MESSAGES

sendMessage("msg1", "Hello")
sendMessage("msg2", "World")
sendMessage("msg3", "How")
sendMessage("msg4", "are")
sendMessage("msg5", "you")
sendMessage("msg6", "today")
sendMessage("msg7", "Jack")
sendMessage("msg8", "and")
sendMessage("msg9", "Jill")
sendMessage("msg10", "went")
sendMessage("msg11", "up")
sendMessage("msg12", "the")


# =============
# splitMessage
# =============
# splits a message into fields
def readMessage(msg):

    # get access global variable
    global messageRaw
    global messageFrom
    global messageSubject
    global messageContent

    messageRaw = msg                    #set raw contents

    # split message
    messageSplit = msg.split(separator)  # split message by message separator symbol

    messageFrom = messageSplit[0]       #set from
    messageSubject = messageSplit[1]    #set subject
    messageContent = messageSplit[2]    #set content














# ================================
# thread for reading network (IN)
# ================================
def networkIN():
    """Thread for listening/reading messages from game server"""

    global message  # get reference to global message variable
    global finished  # get reference to global finished variable

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
    server_socket.bind(('192.168.1.27', 50000))  # bind to this pi's IP address and port 50,000

    while (not finishedNetIN):  # loop until execution halted

        server_socket.listen(1)

        conn, addr = server_socket.accept()  # wait until connection

        while True:
            data = conn.recv(1024)  # receive 1024 bytes (1kb)
            if not data:
                break

            #message = str(data)  # set external message to received data. NOTE: this conversion will be visible but does not work. Needs to be decoded properly like below
            message = data.decode('utf-8', 'replace')  # byte data has to be converted into a character set - 'utf-8' here. 'replace' replaces characters it does not recognise. Was causing comparison prolems "exit" == "exit" was not working. Would show letter 'b' before printing on OLED to denote was raw bytes and hadn't been decoded yet.

            readMessage(message)

        conn.close()  # close connection



















# ==================================
# thread for writing network (OUT)
# ==================================
def networkOUT():
    """sends messages from messageOutBox to game server"""
    #get references to global variables...
    global messageOutBox
    global finished
    global message

    #establish network connection...
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.11', 50000))  # game server IP and Port 50,000

    #client_socket.sendall(str("CONNECTED").encode())
    sendMessage("CONNECTED")



    # debug
    # message = messageOutBox.__len__()

    count = 0

    while not finishedNetOUT:

        if messageOutBox.__len__() > 0:  # messages in outbox?

            nextMessage = messageOutBox.pop()		   # read next message from outbox
            #nextMessage = deviceName + separator + nextMessage       # debug

            #nextMessage = ("python:" + str(count))
            #count = (count + 1)

            # setup network connection
            # --------------------------
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('192.168.1.11', 50000))  # game server IP and Port 50,000

            # send
            # client_socket.sendall(str(id).encode())  # sends RFID tag id to game server
            client_socket.sendall(str(nextMessage).encode())  # sends nextMessage to game server

            # if messageOutBox.__len__() == 0:    # outbox now empty? Close connection...
            # client_socket.close()

            client_socket.close()

            sleep(1)  # slow down 1 sec for debugging






# =============================
# thread for reading RFID Tags
#==============================
def rfidReader():


    #get reference to global variables
    global finished
    global finishedRFID
    global currentSquare
    global previousSquare

    #===========================
    #     CARD READER
    #===========================

    reader = SimpleMFRC522()

    count = 0   #  counter for how many messages are being sent

    while not finishedRFID:

        #reader = SimpleMFRC522()

        try:
            print("=======================")
            print("Place card on reader...")
            print("=======================")
            id, text = reader.read()
            #message = text
            #sendMessage("TagID: " + str(id) + " Read Count: " + str(count))


            if(str(id) != previousSquare):          # throttling - reduces sending messages over network to only when RFID reading different to previous
                sendMessage("TAG", str(id))
                currentSquare = str(id)

            previousSquare = str(id)                # place current reading as previous for keeping history


            count = count + 1
            print("| id: " + str(id))
            print("| text: " + str(text))
            print("=======================")
        finally:
            print("inside finally")
           #GPIO.cleanup()

    GPIO.cleanup()








# ===============
# Start threads
# ===============
netIN = Thread(target=networkIN)
netIN.daemon = True  # thread will yield to closing down
netIN.start()


netOUT = Thread(target=networkOUT)
netOUT.daemon = True
netOUT.start()

rfidIN = Thread(target=rfidReader)
rfidIN.daemon = True
rfidIN.start()







# ===============================
#       DISPLAY LOOP
# ===============================
""" Displays message variable contents"""

while (not finished):



    #if message == "exit":
    if messageRaw == "hst#cmd#exit":

        finishedNetIN = True    # stop netIN thread
        finishedNetOUT = True   # stop netOUT thread
        finishedRFID = True     # stop rfidIN thread
        finished = True         # end looping/execution

        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((5, 40), "Exiting - Bye", fill="white")


        break


    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((5, 5), "From: " + messageFrom, fill="white")
        draw.text((5, 15), "Subj: " + messageSubject, fill="white")
        draw.text((5, 25), "Cont: " + messageContent, fill="white")
        draw.text((5, 35), "RAW: " + messageRaw, fill="white")
        draw.text((5, 50), "RFID: " + str(currentSquare), fill="white")

        # print("******************")
        # print(data.upper())			# prints out message from client in uppercase
        # print("******************")




