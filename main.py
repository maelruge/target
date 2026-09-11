import cv2
import mediapipe as mp


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

img = cv2.imread("ilkkan.jpeg")

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    if not ret:
        break

    HandOpen = False

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]

        uclar = [8, 12, 16, 20]
        eklemler = [6, 10, 14, 18]

        open_leg = 0

        for uc, eklem in zip(uclar, eklemler):
            if hand.landmark[uc].y < hand.landmark[eklem].y:
                open_leg += 1

        if open_leg == 4:
            HandOpen = True
        if HandOpen:

            if img is not None:
                cv2.imshow("img", img)

        else:
            try:
             cv2.destroyWindow("img")
            except cv2.error:
             pass


    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()