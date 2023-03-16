import mediapipe as mp
import pyfirmata
import cv2

# Set up PyFirmata board
board = pyfirmata.Arduino('COM12')
servo_pin = 9  # Change this to the PWM pin connected to the servo
board.digital[servo_pin].mode = pyfirmata.SERVO

# Set up Mediapipe hand detection
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    # Read video from file or camera
    cap = cv2.VideoCapture('4.mp4')  # Change this to your video file path or 0 for webcam

    while cap.isOpened():
        # Get frame from video
        ret, image = cap.read()
        if not ret:
            break

        # Run hand detection
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Check if hand was detected
        if results.multi_hand_landmarks:
            # Get coordinates of pinky tip
            landmarks = results.multi_hand_landmarks[0].landmark
            pinky_tip_x = landmarks[mp_hands.HandLandmark.PINKY_TIP].x

            # Map coordinates to servo angle
            angle = int((pinky_tip_x - 0) * (180 - 0) / (1 - 0) + 0)

            # Send angle to servo
            board.digital[servo_pin].write(angle)

            # Draw hand landmarks on image
            image.flags.writeable = True
            mp_drawing.draw_landmarks(
                image, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
            
        # Show image
        cv2.imshow('Hand Detection', image)
        if cv2.waitKey(10) == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()
