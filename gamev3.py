import cv2
import mediapipe as mp
import numpy as np

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)

# ---------------- HAND MODULE ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ---------------- LOAD BASKET IMAGE ----------------
basket_img = cv2.imread("assets/basket.png", cv2.IMREAD_UNCHANGED)

# ---------------- DRAW BACKGROUND ----------------
def draw_background(img):
    img[:] = (15, 15, 30)  # dark arcade background

    # grid lines (cute game look)
    for i in range(0, img.shape[1], 50):
        cv2.line(img, (i, 0), (i, img.shape[0]), (30, 30, 60), 1)

    for j in range(0, img.shape[0], 50):
        cv2.line(img, (0, j), (img.shape[1], j), (30, 30, 60), 1)

# ---------------- OVERLAY FUNCTION ----------------
def overlay(img, overlay_img, x, y, size=80):
    if overlay_img is None:
        return

    overlay_img = cv2.resize(overlay_img, (size, size))

    h, w = overlay_img.shape[:2]

    for i in range(h):
        for j in range(w):
            if y+i >= img.shape[0] or x+j >= img.shape[1]:
                continue

            if overlay_img.shape[2] == 4:
                alpha = overlay_img[i, j][3] / 255.0
            else:
                alpha = 1

            if alpha > 0:
                img[y+i, x+j] = overlay_img[i, j][:3]

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    draw_background(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    finger_x = finger_y = None

    # ---------------- FINGER DETECTION ----------------
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lm = handLms.landmark

            # INDEX FINGER TIP (LANDMARK 8)
            ix = int(lm[8].x * w)
            iy = int(lm[8].y * h)

            finger_x, finger_y = ix, iy

            # ✨ glowing finger effect
            cv2.circle(frame, (ix, iy), 18, (0, 255, 255), -1)
            cv2.circle(frame, (ix, iy), 10, (0, 150, 255), -1)

            # 🧺 basket overlay on fingertip
            overlay(frame, basket_img, ix - 40, iy - 40, 80)

    # ---------------- UI TEXT ----------------
    cv2.putText(frame, "AR Finger Basket Mode", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)

    cv2.putText(frame, "Move your index finger to control basket", (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)

    # ---------------- SHOW ----------------
    cv2.imshow("GameFlow.cy - Finger Basket", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()