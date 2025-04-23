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




# -----------
# Variables
# -----------
finished = False        # flag for execution stop
message = ""            # holds message received over network
currentSquare = 0       # holds most recently read square (RFID tag serial number)
previousSquare = 0      # holds previous read squire (RFID tag serial number)
messageOutBox = ['msg1', 'msg2', 'msg3', 'msg4', 'msg5', 'msg6', 'msg7', 'msg8', 'msg9', 'msg10']  # holder for messages to be sent





# ============
# sendMessage
# ============
# adds a message to the outbox for sending
def sendMessage(message):
    messageOutBox.append(message)






# ================================
# thread for reading network (IN)
# ================================
def networkIN():
    """Thread for listening/reading messages from game server"""

    global message  # get reference to global message variable
    global finished  # get reference to global finished variable

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
    server_socket.bind(('192.168.1.27', 50000))  # bind to this pi's IP address and port 50,000

    while (not finished):  # loop until execution halted

        server_socket.listen(1)

        conn, addr = server_socket.accept()  # wait until connection

        while True:
            data = conn.recv(1024)  # receive 1024 bytes (1kb)
            if not data:
                break

            #message = str(data)  # set external message to received data. NOTE: this conversion will be visible but does not work. Needs to be decoded properly like below
            message = data.decode('utf-8', 'replace')  # byte data has to be converted into a character set - 'utf-8' here. 'replace' replaces characters it does not recognise. Was causing comparison prolems "exit" == "exit" was not working. Would show letter 'b' before printing on OLED to denote was raw bytes and hadn't been decoded yet.


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

    client_socket.sendall(str("CONNECTED").encode())


    # debug
    # message = messageOutBox.__len__()

    count = 0

    while not finished:

        if messageOutBox.__len__() > 0:  # messages in outbox?

            nextMessage = messageOutBox.pop()		   # read next message from outbox
            nextMessage = "IoTPiece: " + nextMessage       # debug

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
def cardReaderIN():

    #get reference to global variables
    global finished

    #===========================
    #     CARD READER
    #===========================

    reader = SimpleMFRC522()

    count = 0   #  counter for how many messages are being sent

    while not finished:

        #reader = SimpleMFRC522()

        try:
            print("=======================")
            print("Place card on reader...")
            print("=======================")
            id, text = reader.read()
            #message = text
            sendMessage("TagID: " + str(id) + " Read Count: " + str(count))
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

cardIN = Thread(target=cardReaderIN)
cardIN.daemon = True
cardIN.start()



# ===============================
#       DISPLAY LOOP
# ===============================
""" Displays message variable contents"""

while (not finished):



    if message == "exit":
        finished = True  # end looping/execution
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((5, 40), "Exiting - Bye", fill="white")


    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((5, 40), "MSG: " + message, fill="white")

        # print("******************")
        # print(data.upper())			# prints out message from client in uppercase
        # print("******************")




