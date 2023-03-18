import cv2
import mediapipe as mp
import time
import pyfirmata

# Setup Arduino board
board = pyfirmata.Arduino('COM5')
servo_pin = board.get_pin('d:8:s')
servo_initial_pos = 0

# Set up video capture
cap = cv2.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Set up Pose detection
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    last_right_knee_pos = None
    last_right_knee_movement = 0
    while True:
        # Read the frame from the camera
        success, image = cap.read()

        # Break the loop if the video has ended
        if not success:
            break

        # Convert the image from BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image and detect pose landmarks
        results = pose.process(image)

        # Draw pose landmarks on the image
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Get the right knee landmarks
            right_knee_landmarks = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]

            # Get the y coordinate of the right knee landmark
            right_knee_y = right_knee_landmarks.y * image.shape[0]

            # Check if there is a previous right knee position
            if last_right_knee_pos is not None:
                # Calculate the difference in the right knee position
                right_knee_diff = right_knee_y - last_right_knee_pos

                # Apply smoothing to right knee movement
                right_knee_movement = (right_knee_diff - last_right_knee_movement) * 0.5
                last_right_knee_movement = right_knee_diff

                # Check if the right knee is bent
                if right_knee_movement < -5:
                    servo_pos = 140
                    servo_pin.write(servo_pos)
                    time.sleep(0.1)

                # Check if the right knee is straight
                elif right_knee_movement > 5:
                    servo_pos = servo_initial_pos
                    servo_pin.write(servo_pos)
                    time.sleep(0.1)

            # Set the current right knee position as the last position
            last_right_knee_pos = right_knee_y

        # Show the image
        cv2.imshow('Right Knee Detection', image)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
