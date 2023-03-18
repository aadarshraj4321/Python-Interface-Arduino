import mediapipe as mp
import pyfirmata
import cv2

# Set up PyFirmata board
board = pyfirmata.Arduino('COM5')
servo_pin = 9  # Change this to the PWM pin connected to the servo
board.digital[servo_pin].mode = pyfirmata.SERVO

# Set up Mediapipe pose detection
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    # Initialize variables for detecting elbow swing
    left_elbow_in_motion = None
    left_elbow_threshold = 20.0

    # Set up camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    while True:
        # Get image from webcam
        ret, image = cap.read()
        if not ret:
            continue

        # Flip image horizontally for natural-looking video
        image = cv2.flip(image, 1)

        # Resize image for faster processing
        image_resized = cv2.resize(image, (640, 480))

        # Run pose detection on resized image
        image_resized = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
        results = pose.process(image_resized)

        # Check if left elbow is swinging
        if results.pose_landmarks:
            left_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
            left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]

            # Calculate the difference in y-coordinates between elbow and wrist
            left_elbow_motion = abs(left_elbow.y * 480 - left_wrist.y * 480)
            left_elbow_in_motion = left_elbow_motion > left_elbow_threshold

            # Rotate servo if left elbow is in motion
            if left_elbow_in_motion:
                board.digital[servo_pin].write(80)  # Change this to your desired servo angle
            else:
                board.digital[servo_pin].write(140)  # Set servo to 0 degrees

            # Draw pose landmarks on image
            mp_drawing.draw_landmarks(
                image_resized, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Display image
        cv2.imshow('Pose Detection', image_resized)
        if cv2.waitKey(10) == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()
