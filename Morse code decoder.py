import cv2
import mediapipe as mp
import time

# Initialize Mediapipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Initialize Camera
cap = cv2.VideoCapture(0)

# Morse Code Dictionary
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9'
}

# Variables for tap detection
morse_code = ""
decoded_text = ""
current_letter = ""
prev_y = None
tap_start_time = 0
finger_down = False
detecting = False
last_tap_time = time.time()
last_letter_time = time.time()
last_word_time = time.time()

# Sensitivity Parameters
VELOCITY_THRESHOLD = 15  # Increased to filter unintentional movement
DOT_HOLD_THRESHOLD = 0.25
DASH_HOLD_THRESHOLD = 0.55
MIN_MOVEMENT_THRESHOLD = 10  # Ensures enough vertical displacement before detecting a tap

print("🚀 Ready! Press 'd' to Start Detection | 'r' to Reset | 'q' to Quit")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process hands
    result = hands.process(rgb_frame)
    fingertip_y = None

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get index finger tip coordinates
            fingertip = hand_landmarks.landmark[8]
            h, w, _ = frame.shape
            fingertip_y = int(fingertip.y * h)

            # Draw fingertip marker
            cv2.circle(frame, (int(fingertip.x * w), fingertip_y), 10, (0, 255, 0), -1)

            if detecting:
                if prev_y is not None:
                    velocity = fingertip_y - prev_y

                    # Detect downward motion (tap start)
                    if velocity > VELOCITY_THRESHOLD and not finger_down and abs(fingertip_y - prev_y) > MIN_MOVEMENT_THRESHOLD:
                        tap_start_time = time.time()
                        finger_down = True
                        print("🟢 Tap STARTED!")

                    # Detect upward motion (tap end)
                    elif velocity < -VELOCITY_THRESHOLD and finger_down:
                        tap_duration = time.time() - tap_start_time
                        finger_down = False
                        print(f"🛑 Tap ENDED! Duration: {tap_duration:.2f} sec")

                        if tap_duration < DOT_HOLD_THRESHOLD:
                            current_letter += '.'
                            print("✅ Detected: DOT (.)")
                        elif tap_duration > DASH_HOLD_THRESHOLD:
                            current_letter += '-'
                            print("✅ Detected: DASH (-)")

                        last_tap_time = time.time()
                        last_letter_time = time.time()

                prev_y = fingertip_y  # Update previous Y position

    # Handle letter detection (gaps)
    if detecting and time.time() - last_letter_time > 1.2 and current_letter:
        decoded_char = MORSE_CODE_DICT.get(current_letter, '?')
        decoded_text += decoded_char
        print(f"🔠 Letter Decoded: {decoded_char} (From {current_letter})")
        morse_code += current_letter + " "
        current_letter = ""

    # Handle word detection (longer gaps)
    if detecting and time.time() - last_letter_time > 2.0 and decoded_text and last_word_time != last_letter_time:
        decoded_text += " "
        last_word_time = last_letter_time
        print("📖 Word Gap Detected!")

    # Display results
    cv2.putText(frame, f"Morse Code: {morse_code}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, f"Decoded: {decoded_text}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, "Press 'd' to Start/Stop | 'r' to Reset | 'q' to Quit", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Finger Tap Morse Code", frame)

    # Handle key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Quit
        break
    elif key == ord('d'):  # Toggle Detection Mode
        detecting = not detecting
        print(f"⚡ Detection Mode: {'ON' if detecting else 'OFF'}")
    elif key == ord('r'):  # Reset
        morse_code = ""
        decoded_text = ""
        current_letter = ""
        print("🔄 Reset! Ready for new input.")

cap.release()
cv2.destroyAllWindows()
