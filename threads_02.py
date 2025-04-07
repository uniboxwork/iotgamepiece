# =====================================================================================
#  Will display message received from thread listening for network connections
# =====================================================================================


# --------------------
# OLED SCREEN IMPORTS
# --------------------
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, sh1107, ws0010
from time import sleep

# -----------------
# Network imports
# -----------------
import socket


# ---------------
# Thread imports
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
finished = False    # flag for execution stop
message = ""        # holds message received over network
currentSquare = 0   # holds most recently read square (RFID tag serial number)
messageOutBox = ['msg1','msg2','msg3','msg4','msg5','msg6','msg7','msg8', 'msg9', 'msg10']  # holder for messages to be sent



#================================
# thread for reading network (IN)
#================================
def networkIN():
    """Thread for listening/reading messages from game server"""

    global message      # get reference to global message variable
    global finished     # get reference to global finished variable

    while (not finished):       # loop until execution halted

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # create socket
        server_socket.bind(('192.168.1.27', 50000))                         # bind to this pi's IP address and port 50,000
        server_socket.listen(1)

        conn, addr = server_socket.accept()  # wait until connection

        while True:
            data = conn.recv(1024)          # receive 1024 bytes (1kb)
            if not data:
                break

            message = str(data)             # set external message to received data

        conn.close()                        # close connection


# ==================================
# thread for writing network (OUT)
# ==================================
def networkOUT():
    """Thread for sending messages to game server"""
    global messageOutBox    # get reference to outbox
    global finished
    global message

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.11', 50000))  # game server IP and Port 50,000
    client_socket.sendall(str("CONNECTED").encode())  # sends nextMessage to game server
    #client_socket.close()

    #debug
    #message = messageOutBox.__len__()

    while not finished :

        if messageOutBox.__len__() > 0 :      # messages in outbox?
            nextMessage = messageOutBox.pop()
            message = nextMessage               # debug
            # setup network connection
            # --------------------------
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('192.168.1.11', 50000))      # game server IP and Port 50,000

            # send
            #client_socket.sendall(str(id).encode())  # sends RFID tag id to game server
            client_socket.sendall(str(nextMessage).encode())  # sends nextMessage to game server

            if messageOutBox.__len__() == 0:    # outbox now empty? Close connection...
                client_socket.close()

            sleep(3) # slow down for debugging





# ===============
# Start threads
# ===============
netIN = Thread(target=networkIN)
netIN.daemon = True     # thread will yield to closing down
netIN.start()


# Connnect once to game server...

"""
greeting = "bonjour"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.11', 50000))  # game server IP and Port 50,000
client_socket.sendall(greeting.encode())  # sends nextMessage to game server
client_socket.close()
"""




netOUT = Thread(target=networkOUT)
netOUT.daemon = True
netOUT.start()









# ===============================
#       DISPLAY LOOP
# ===============================
""" Displays message variable contents"""

while (not finished):

    if message == "exit":
        finished = True     # end looping/execution


    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((30, 40), "MESSAGE: " + str(message), fill="white")

        # print("******************")
        # print(data.upper())			# prints out message from client in uppercase
        # print("******************")






