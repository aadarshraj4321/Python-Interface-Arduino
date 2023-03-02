import cv2
import numpy as np
from pyfirmata import Arduino, util
from time import sleep

cap = cv2.VideoCapture(0)
#board = Arduino('COM5') 

## Create Trackbar

HueLow = 0
HueHigh = 20
SatLow = 0
SatHigh = 10
ValLow = 0
ValHigh = 10
global carOn
carOn = False

def onTrackHueLow(val):
    global HueLow;
    HueLow = val
    print("HueLow : ", val)


def onTrackHueHigh(val):
    global HueHigh;
    HueHigh = val
    print("HueHigh : ", val)



def onTrackSatLow(val):
    global SatLow;
    SatLow = val
    print("SatLow : ", val)




def onTrackSatHigh(val):
    global SatHigh;
    SatHigh = val
    print("SatHigh : ", val)


def onTrackValLow(val):
    global ValLow;
    ValLow = val
    print("ValLow : ", val)



def onTrackValHigh(val):
    global ValHigh;
    ValHigh = val
    print("ValHigh : ", val)




cv2.namedWindow("objectTracker")
cv2.createTrackbar("HueLow", "objectTracker", 78, 179, onTrackHueLow)
cv2.createTrackbar("HueHigh", "objectTracker", 179, 179, onTrackHueHigh)
cv2.createTrackbar("SatLow", "objectTracker", 105, 255, onTrackSatLow)
cv2.createTrackbar("SatHigh", "objectTracker", 187, 255, onTrackSatHigh)
cv2.createTrackbar("ValLow", "objectTracker", 204, 255, onTrackValLow)
cv2.createTrackbar("ValHigh", "objectTracker", 255, 255, onTrackValHigh)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (400, 300))
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerBound = np.array([HueLow, SatLow, ValLow])
    upperBound = np.array([HueHigh, SatHigh, ValHigh])
    mask = cv2.inRange(frameHSV, lowerBound, upperBound)
    invereMask = cv2.bitwise_not(mask)
    detectTheObject = cv2.bitwise_and(frame, frame, mask = mask)

    if((HueLow >= 40 or HueLow <= 50) and (HueHigh >= 170 or HueHigh <= 185) and (SatLow >= 3 or SatLow <= 9) and (SatHigh >= 180 or SatHigh <= 192) and (ValLow >= 128 or ValLow <= 140) and (ValHigh >= 245)):
        print("Servo Motor On")
##        sleeTime = 0.03
##        
##        ledPinOne = 8
##        ledPinTwo = 9
##        ledPinThree = 10
##            
##        board.digital[ledPinOne].write(1)
##        sleep(sleeTime)
##        board.digital[ledPinOne].write(0)
##        sleep(sleeTime)
##
##        board.digital[ledPinTwo].write(1)
##        sleep(sleeTime)
##        board.digital[ledPinTwo].write(0)
##        sleep(sleeTime)
##
##        board.digital[ledPinThree].write(1)
##        sleep(sleeTime)
##        board.digital[ledPinThree].write(0)
##        sleep(sleeTime)

    
    cv2.imshow("frame", frame)
    cv2.imshow("frameHSV", frameHSV)
    cv2.imshow("mask", mask)
    cv2.imshow("detectTheObject", detectTheObject)
    cv2.imshow("inverseMask", invereMask)

    if(cv2.waitKey(2) & 0xff == ord('f')):
        break

cap.release()
cv2.destroyAllWindows()
