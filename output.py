import cv2
import mediapipe as mp
from detector import analyze_hand_movements, detect_hands, calculate_distance
# Initialize MediaPipe hands solution
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Capture video from camera
cap = cv2.VideoCapture('./video_samples/hand_video_3.mp4')




# Main loop for video processing
while True:
    success, image = cap.read()
    if not success:
        break

    # Convert BGR image to RGB for MediaPipe
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect hands in the image
    results = detect_hands(image)

    # Draw detected hands on the image
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Analyze hand movements
    output = analyze_hand_movements(results)
    print(output)
    # Display the processed image
    cv2.imshow('Hand Detection', image)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()