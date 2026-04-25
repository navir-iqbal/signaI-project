import cv2
import mediapipe as mp
import time

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

def start_camera(duration=5):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return "Camera Error"

    start_time = time.time()
    detected_text = "No Hand"
    prev_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip for natural mirror view
        frame = cv2.flip(frame, 1)

        # Convert to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        # Default state
        detected_text = "No Hand"

        if result.multi_hand_landmarks:
            detected_text = "Hand Detected"

            for handLms in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame,
                    handLms,
                    mp_hands.HAND_CONNECTIONS
                )

        # FPS calculation
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
        prev_time = curr_time

        # -------- UI Overlay --------
        # Background box
        cv2.rectangle(frame, (10, 10), (320, 110), (0, 0, 0), -1)

        # Status text
        cv2.putText(
            frame,
            f"Status: {detected_text}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        # FPS text
        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1
        )

        # Exit instruction
        cv2.putText(
            frame,
            "ESC to exit",
            (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (200, 200, 200),
            1
        )

        # Show camera window
        cv2.imshow("SignAI Camera", frame)

        # Stop after fixed duration (important for backend)
        if time.time() - start_time > duration:
            break

        # Exit manually
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return detected_text