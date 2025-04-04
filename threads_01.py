# =====================================================================================
#  Will display message received by thread listening for network connections
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
messageOutBox = []  #






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





# Start threads

netIN = Thread(target=networkIN)
netIN.daemon = True     # thread will yield to closing down
netIN.start()







# ===============================
#       DISPLAY LOOP
# ===============================
""" Displays message variable contents"""

while (not finished):

    if message == "exit":
        finished = True     # end looping/execution


    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((30, 40), "MESSAGE: " + message, fill="white")

        # print("******************")
        # print(data.upper())			# prints out message from client in uppercase
        # print("******************")






