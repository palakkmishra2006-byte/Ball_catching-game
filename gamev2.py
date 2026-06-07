import cv2
import mediapipe as mp
import random
import math

# ---------------- HAND TRACKING ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

# ---------------- BALLS ----------------
balls = []
for _ in range(6):
    balls.append([
        random.randint(50, 600),
        random.randint(-300, 0),
        random.randint(5, 12)
    ])

score_left = 0
score_right = 0

# ---------------- DISTANCE ----------------
def dist(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

# ---------------- SPLASH EFFECT ----------------
def splash(img, x, y, color):
    for _ in range(15):
        px = x + random.randint(-25, 25)
        py = y + random.randint(-25, 25)
        cv2.circle(img, (px, py), 3, color, -1)

# ---------------- MAIN LOOP ----------------
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    left_x = left_y = None
    right_x = right_y = None

    # ---------------- HAND DETECTION ----------------
    if result.multi_hand_landmarks and result.multi_handedness:
        for idx, handLms in enumerate(result.multi_hand_landmarks):
            label = result.multi_handedness[idx].classification[0].label
            lm = handLms.landmark

            ix = int(lm[8].x * w)
            iy = int(lm[8].y * h)

            if label == "Left":
                left_x, left_y = ix, iy
                cv2.circle(img, (left_x, left_y), 15, (255, 0, 0), -1)

            elif label == "Right":
                right_x, right_y = ix, iy
                cv2.circle(img, (right_x, right_y), 15, (0, 255, 0), -1)

    # ---------------- BALL LOGIC ----------------
    for ball in balls:
        ball[1] += ball[2]

        if ball[1] > h:
            ball[0] = random.randint(50, w-50)
            ball[1] = random.randint(-200, 0)
            ball[2] = random.randint(5, 12)

        cv2.circle(img, (ball[0], ball[1]), 12, (0, 0, 255), -1)

        caught = False

        # ---------------- LEFT HAND CATCH ----------------
        if left_x is not None:
            if dist(left_x, left_y, ball[0], ball[1]) < 35:
                score_left += 1
                splash(img, ball[0], ball[1], (255, 0, 0))
                caught = True

        # ---------------- RIGHT HAND CATCH ----------------
        if not caught and right_x is not None:
            if dist(right_x, right_y, ball[0], ball[1]) < 35:
                score_right += 1
                splash(img, ball[0], ball[1], (0, 255, 0))
                caught = True

        if caught:
            ball[0] = random.randint(50, w-50)
            ball[1] = random.randint(-200, 0)

    # ---------------- UI ----------------
    cv2.putText(img, f"Left Score: {score_left}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    cv2.putText(img, f"Right Score: {score_right}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.putText(img, "GameFlow.cy Dual Hand Mode", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

    cv2.imshow("GameFlow.cy", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()