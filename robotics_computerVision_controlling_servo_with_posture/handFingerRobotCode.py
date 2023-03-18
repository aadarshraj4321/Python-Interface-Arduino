import mediapipe as mp
import pyfirmata
import cv2

# Set up PyFirmata board
board = pyfirmata.Arduino('COM5')
servo_pin = 11  # Change this to the PWM pin connected to the servo
board.digital[servo_pin].mode = pyfirmata.SERVO

# Set up Mediapipe hand detection
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    # Read video from file or camera
    cap = cv2.VideoCapture(0)  # Change this to your video file path or 0 for webcam

    # Initialize variables for detecting hand gestures
    hand_crunch = False
    fingers_extended = False
    fingers_extended_threshold = 0.9

    while cap.isOpened():
        # Get frame from video
        ret, image = cap.read()
        if not ret:
            break

        # Run hand detection
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Check for hand gestures
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Check if fingers are extended
                finger_tips = [
                    hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                    hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                    hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                    hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                ]
                fingers_extended = all(tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y for tip in finger_tips)

                # Check if hand is in a "crunch" position
                hand_crunch = (
                    hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x > hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x and
                    hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
                )

                # Rotate servo based on hand gesture
                if hand_crunch:
                    board.digital[servo_pin].write(80)  # Set servo to 0 degrees
                    print("60 degree")
                elif fingers_extended:
                    board.digital[servo_pin].write(180)  # Change this to your desired servo angle
                    print("140 degree")

                # Draw hand landmarks on image
                image.flags.writeable = True
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Show image
        cv2.imshow('Hand Detection', image)
        if cv2.waitKey(10) == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()
