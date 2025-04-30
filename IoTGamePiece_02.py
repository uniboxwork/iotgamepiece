# =====================================================================================
#  IoT Game Piece - v0.1
# =====================================================================================
"""
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

# sys message test...
sendMessage("sys", "start")
sendMessage("sys", "pause")
sendMessage("sys", "resume")
sendMessage("sys", "restart")
sendMessage("sys", "end")


# TAG message test...
sendMessage("TAG", "584604745789")
sendMessage("TAG", "584604680242")
sendMessage("TAG", "584604614707")
sendMessage("TAG", "584604483633")
sendMessage("TAG", "584615428318")
sendMessage("TAG", "584615362783")
sendMessage("TAG", "584606887152")
sendMessage("TAG", "584615166162")
sendMessage("TAG", "584615231709")
sendMessage("TAG", "584615558951")
sendMessage("TAG", "584615821115")
sendMessage("TAG", "584615624484")
sendMessage("TAG", "584615690021")
sendMessage("TAG", "584615755578")
sendMessage("TAG", "584604155914")
sendMessage("TAG", "584604221493")
sendMessage("TAG", "584604287028")
sendMessage("TAG", "584604352567")
sendMessage("TAG", "584604418102")
sendMessage("TAG", "584604549168")

"""


        
        for samples...
        tagMappings.put("584604745789",1);
        tagMappings.put("584604680242",2);
        tagMappings.put("584604614707",3);
        tagMappings.put("584604483633",4);
        tagMappings.put("584615428318",5);
        tagMappings.put("584615362783",6);
        tagMappings.put("584606887152",7);
        tagMappings.put("584615166162",8);
        tagMappings.put("584615231709",9);
        tagMappings.put("584615558951",10);
        tagMappings.put("584615821115",11);
        tagMappings.put("584615624484",12);
        tagMappings.put("584615690021",13);
        tagMappings.put("584615755578",14);
        tagMappings.put("584604155914",15);
        tagMappings.put("584604221493",16);
        tagMappings.put("584604287028",17);
        tagMappings.put("584604352567",18);
        tagMappings.put("584604418102",19);
        tagMappings.put("584604549168",20);
         


"""




"""
sendMessage("msg1", "Hello")
sendMessage("msg2", "World")
sendMessage("msg3", "the")
sendMessage("msg4", "quick")
sendMessage("msg5", "brown")
sendMessage("msg6", "fox")
sendMessage("msg7", "jumps")
sendMessage("msg8", "over")
sendMessage("msg9", "the")
sendMessage("msg10", "lazy")
sendMessage("msg11", "dog")
sendMessage("msg12", "the")
"""

# =============
# readMessage
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

        #global messageFrom      #debug
        #messageFrom = str(messageOutBox.__len__())            #debug - display in 'from: ' box

        if messageOutBox.__len__() > 0:  # messages in outbox?

            #nextMessage = messageOutBox.pop()		   # read next message from outbox - reads from last place in stack
            nextMessage = messageOutBox.pop(0)         # read next message from outbox - reads form the first place


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




