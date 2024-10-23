import cv2
import mediapipe as mp

# Initialize MediaPipe hands solution
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Capture video from camera
cap = cv2.VideoCapture('./video_samples/hand_video_3.mp4')

# Define functions for hand detection and movement analysis
def detect_hands(image):
    results = hands.process(image)
    return results

def analyze_hand_movements(results):
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract key points for hand analysis
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # Calculate distances between fingertips
            thumb_index_distance = calculate_distance(thumb_tip, index_tip)
            index_middle_distance = calculate_distance(index_tip, middle_tip)
            middle_ring_distance = calculate_distance(middle_tip, ring_tip)
            ring_pinky_distance = calculate_distance(ring_tip, pinky_tip)

            # Analyze hand movements based on distance thresholds
            x = 'a'
            if thumb_index_distance < threshold:
                x = "Hand is closed"
            elif thumb_index_distance > threshold and index_middle_distance < threshold and middle_ring_distance < threshold and ring_pinky_distance < threshold:
                x = "Hand is making a fist"
            elif index_tip.y < middle_tip.y and index_tip.y < ring_tip.y and index_tip.y < pinky_tip.y:
                x = "Bhai galat baat !!"
            else:
                x = "Hand is open"
        return x

def calculate_distance(point1, point2):
    x1, y1, z1 = point1.x, point1.y, point1.z
    x2, y2, z2 = point2.x, point2.y, point2.z
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
    return distance

# Set threshold for hand movements
threshold = 0.05

