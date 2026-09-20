import cv2
import mediapipe as mp
import tkinter as tk

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()




pencere = tk.Tk()
pencere.title("Giriş")
pencere.geometry("350x180+655+440")

x_merkez = (screen_width - 900) // 2
y_merkez = ((screen_height - 480) // 2) - 150

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

img = cv2.imread("ilkkan.jpeg")
camera = cv2.VideoCapture(0)

cv2.namedWindow("Camera")
cv2.moveWindow("Camera", x_merkez, y_merkez)

uclar = [8, 12, 16, 20]
eklemler = [6, 10, 14, 18]

while True:
    ret, frame = camera.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    HandOpenNumber = 0

    if result.multi_hand_landmarks and len(result.multi_hand_landmarks) == 2:

        for hand in result.multi_hand_landmarks:
            open_finger = 0

            for uc, eklem in zip(uclar, eklemler):
                if hand.landmark[uc].y < hand.landmark[eklem].y:
                 open_finger += 1

            if open_finger == 4:
                 HandOpenNumber += 1

    if HandOpenNumber == 2:
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
pencere.mainloop()