# =====================================================================================
# python basic server - receives message from game server and displays on OLED screen
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

# ===========================
#     OLED DISPLAY SETUP
# ===========================
serial = i2c(port=1, address=0x3c)
device = sh1106(serial)

while True:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.1.27', 50000))     # this pi's IP address and port 50,000
    # server_socket.bind(('192.168.1.11', 50000))
    # server_socket.bind(('0.0.0.0', 50000))
    server_socket.listen(1)

    # print("Server is waiting for connections...")
    # conn, addr = server_socket.accept()			# will wait until connection
    # print(f"Connected by {addr}")

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        # draw.text((30, 40), "Hello World!", fill="white")
        # draw.text((30, 40), message, fill="white")
        draw.text((30, 40), "Server is waiting for connections...", fill="white")

    # sleep(3)

    conn, addr = server_socket.accept()  # will wait until connection

    while True:
        data = conn.recv(1024)
        if not data:
            break

        # print("******************")
        # print(data.upper())			# prints out message from client in uppercase
        # print("******************")
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            # draw.text((30, 40), "Hello World!", fill="white")
            # draw.text((30, 40), message, fill="white")
            draw.text((30, 40), str(data), fill="white")

    sleep(3)

    conn.close()

