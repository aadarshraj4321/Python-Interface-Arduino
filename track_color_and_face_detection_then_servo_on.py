
import numpy as np
import cv2
from pyfirmata import Arduino, util
from time import sleep


# Capturing video through webcam
cap = cv2.VideoCapture(0)
board = Arduino("COM5")
motorWheel = 10


## Face Detection Haarcascade
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Start a while loop
while True:

    board.digital[motorWheel].write(0)
    ret, imageFrame = cap.read()
    imageFrame = cv2.resize(imageFrame, (400, 300))
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)


    ## Face Detection Part
    grayFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY)
    allFaces = faceCascade.detectMultiScale(grayFrame, 1.3, 5)

    # Set range for red color and
    # define mask
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    # Set range for gray color and
    # define mask
    gray_lower = np.array([0, 0, 0], np.uint8)
    gray_upper = np.array([0, 0, 50], np.uint8)
    gray_mask = cv2.inRange(hsvFrame, gray_lower, gray_upper)

    # Set range for green color and
    # define mask
    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    # Set range for blue color and
    # define mask
    blue_lower = np.array([94, 30, 2], np.uint8)
    blue_upper = np.array([120, 100, 100], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    # Set range for black color and define mask
    black_lower = np.array([0, 0, 0], np.uint8)
    black_upper = np.array([10, 10, 10], np.uint8)
    black_mask = cv2.inRange(hsvFrame, black_lower, black_upper)
    
    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")
        
    # For red color
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(imageFrame, imageFrame,
                                                            mask = red_mask)


    # For gray color
    gray_mask = cv2.dilate(gray_mask, kernal)
    res_gray = cv2.bitwise_and(imageFrame, imageFrame,
                                                            mask = gray_mask)


    # For black color
    black_mask = cv2.dilate(black_mask, kernal)
    res_black = cv2.bitwise_and(imageFrame, imageFrame,
                                                            mask = black_mask)
    # For green color
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(imageFrame, imageFrame,
                                                                    mask = green_mask)
            
    # For blue color
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(imageFrame, imageFrame,
                                                            mask = blue_mask)





    # Creating contour to track black color
    contours, hierarchy = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
    for pic, contour in enumerate(contours):
        
        sleeTime = 0.03
        area = cv2.contourArea(contour)
        
        if(area > 300):
            board.digital[motorWheel].write(1)
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),(x + w, y + h),(255, 255, 255), 2)
                        
            cv2.putText(imageFrame, "Black Colour", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255))
                








    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask,
                                                                                    cv2.RETR_TREE,
                                                                                    cv2.CHAIN_APPROX_SIMPLE)
            
    for pic, contour in enumerate(contours):
        
        sleeTime = 0.03
        area = cv2.contourArea(contour)
        
        if(area > 300):
            for face in allFaces:
                if(x is not None and y is not None and w is not None and h is not None):
                    cv2.rectangle(imageFrame, ())
                    x, y, w, h = cv2.boundingRect(contour)
                    imageFrame = cv2.rectangle(imageFrame, (x, y),(x + w, y + h),(0, 0, 255), 2)    
                    cv2.putText(imageFrame, "Red Colour", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255))






    # Creating contour to track gray color
    contours, hierarchy = cv2.findContours(gray_mask,
                                                                                    cv2.RETR_TREE,
                                                                                    cv2.CHAIN_APPROX_SIMPLE)
            
    for pic, contour in enumerate(contours):
        
        sleeTime = 0.03
        area = cv2.contourArea(contour)
        
        if(area > 300):
            board.digital[motorWheel].write(1)
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),(x + w, y + h),(0, 0, 255), 2)
                        
            cv2.putText(imageFrame, "Gray Colour", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255))

                

        # Creating contour to track green color
        contours, hierarchy = cv2.findContours(green_mask,
                                                                                cv2.RETR_TREE,
                                                                                cv2.CHAIN_APPROX_SIMPLE)
        
    for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                    x, y, w, h = cv2.boundingRect(contour)
                    imageFrame = cv2.rectangle(imageFrame, (x, y),
                                                                    (x + w, y + h),
                                                                    (0, 255, 0), 2)
                    
                    cv2.putText(imageFrame, "Green Colour", (x, y),
                                                cv2.FONT_HERSHEY_SIMPLEX,
                                                1.0, (0, 255, 0))

            # Creating contour to track blue color
            contours, hierarchy = cv2.findContours(blue_mask,
                                                                                    cv2.RETR_TREE,
                                                                                    cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if(area > 300):
                            board.digital[motorWheel].write(1)
                            x, y, w, h = cv2.boundingRect(contour)
                            imageFrame = cv2.rectangle(imageFrame, (x, y),
                                                                            (x + w, y + h),
                                                                            (255, 0, 0), 2)
                            
                            cv2.putText(imageFrame, "Blue Colour", (x, y),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    1.0, (255, 0, 0))

            canny = cv2.Canny(imageFrame, 80, 60)               
            # Program Termination
            cv2.imshow("hsvFrame", hsvFrame)
            cv2.imshow("red_mask", red_mask)
            cv2.imshow("green_mask", green_mask)
            cv2.imshow("blue_mask", blue_mask)
            cv2.imshow("black_mask", black_mask)
            cv2.imshow("canny", canny)
            cv2.imshow("Aman Seat Belt Detection", imageFrame)
            if cv2.waitKey(1) & 0xFF == ord('f'):
                break

cap.release()
cv2.destroyAllWindows()
