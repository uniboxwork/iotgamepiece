
#=====================
# IoT Game Piece v0.1
#=====================

import time
from threading import Thread

startTime = time.time()           #holds the time of the games beginning (in seconds since Unix epoch)


#-----------------
# State Variables
#-----------------
hoursOfStudy = 0        #holds score of hours dedicated to study (the higher the better)
timeRemaining = 72      #the time until the project deadline
finished = False        #controller for the game loop


def addHoursOfStudy(hrs=1):
    self.hoursOfStudy += hrs


def removeHoursOfStudy(hrs=1):
    self.hoursOfStudy -= hrs


def calculateGrade():
    # calculate the players grade from the hours of study
    finalGrade = 0



def calculateTimeRemaining():
        """calculates time remaining in the game. (if not using the threaded solution)"""

        # seconds since game start
        secondsElapsed = time.time() - startTime

        # minutes since game start (rounded)
        minutesElapsed = int(secondsElapsed / 60)

        # different from last check?

        # subtracted from time remaining
        timeRemaining -= minutesElapsed


def timeReductionThread():
    """reduces the remaining game time every minute"""

    global timeRemaining    # get access to global variable (outside this thread)

    print("*******************************")
    print(" timeReductionThread STARTED")
    print("*******************************")

    while(True):
        time.sleep(5)  # wait 5 seconds
        print(f"Reducing time")
        timeRemaining -= 1




# Thread for RFID reader - send message of change



# start time reduction thread
t1 = Thread(target=timeReductionThread)
t1.start()







# Game Loop
while (not finished):       #loop until game finished

    #read time
    #calculate time remaining
    #out of time?
    #messages?
    #read RFID
    #Any change? - report

    print(f"Time remaining: {timeRemaining}")
    time.sleep(6)

