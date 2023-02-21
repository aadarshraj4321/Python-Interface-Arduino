
from pyfirmata import Arduino, util
from time import sleep
from open_cv_python_arduino_one import carOn

sleeTime = 0.03
board = Arduino('COM5') # Change to your port
ledPinOne = 8
ledPinTwo = 9
ledPinThree = 10
while carOn == True:
    board.digital[ledPinOne].write(1)
    sleep(sleeTime)
    board.digital[ledPinOne].write(0)
    sleep(sleeTime)

    board.digital[ledPinTwo].write(1)
    sleep(sleeTime)
    board.digital[ledPinTwo].write(0)
    sleep(sleeTime)

    board.digital[ledPinThree].write(1)
    sleep(sleeTime)
    board.digital[ledPinThree].write(0)
    sleep(sleeTime)
