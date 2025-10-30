import cv2
import mediapipe as mp
import pyttsx3
import socket
import math

# Initialize libraries
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)
engine = pyttsx3.init()

# Connect to Java Display
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5000))

cap = cv2.VideoCapture(0)

def speak(text):
    print(f"[SPEAK] {text}")
    engine.say(text)
    engine.runAndWait()
    client.send((text + "\n").encode())  # Send to Java

while True:
    success, img = cap.read()
    if not success:
        continue
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    recognized_text = "No Gesture"

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get landmarks
            tips = [mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP,
                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP,
                    mp_hands.HandLandmark.PINKY_TIP]
            
            tip_coords = [(hand_landmarks.landmark[t].x, hand_landmarks.landmark[t].y) for t in tips]
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

            # Simple gesture logic (based on relative positions)
            thumb_y, index_y, middle_y, ring_y, pinky_y = [t[1] for t in tip_coords]

            # ✊ STOP - All fingers up (open palm)
            if (thumb_y < wrist.y and index_y < wrist.y and
                middle_y < wrist.y and ring_y < wrist.y and pinky_y < wrist.y):
                recognized_text = "Stop"

            # 👍 LIKE - Thumb up higher than index
            elif thumb_y < index_y:
                recognized_text = "Like"

            # 👋 HELLO - Only index & middle raised (like V shape)
            elif (index_y < wrist.y and middle_y < wrist.y and
                  ring_y > wrist.y and pinky_y > wrist.y):
                recognized_text = "Hello"

            # ✌️ PEACE - Index and middle up, others down
            elif (index_y < wrist.y and middle_y < wrist.y and
                  ring_y > wrist.y and pinky_y > wrist.y):
                recognized_text = "Peace"

            # 🙏 THANK YOU - All fingers close (fist)
            elif (index_y > wrist.y and middle_y > wrist.y and
                  ring_y > wrist.y and pinky_y > wrist.y):
                recognized_text = "Thank You"

            # Display and speak
            cv2.putText(img, recognized_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            speak(recognized_text)

    cv2.imshow("Gesture Recognition", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
