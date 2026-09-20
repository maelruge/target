import tkinter as tk
import cv2
import mediapipe as mp

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


x_merkez = (screen_width - 900) // 2
y_merkez = ((screen_height - 480) // 2) - 150

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)


camera = cv2.VideoCapture(0)

cv2.namedWindow("Camera")
cv2.moveWindow("Camera", x_merkez, y_merkez)

uclar = [8, 12, 16, 20]
eklemler = [6, 10, 14, 18]

root = tk.Tk()
root.title("enter")
root.geometry("350x180+655+440")

def Start_Camera():
    root.destroy()  # Tkinter'ı tamamen kapatıp belleği serbest bırak
    targetHand(uclar, eklemler)


def kontrol():
    cevap = kutu.get().strip().lower()
    if cevap == "rüzgar":
        sonuc.config(text="Ellerini kaldır!", fg="red")
        root.after(2000,Start_Camera)

    else:
        sonuc.config(text="GEÇ.", fg="green")



def targetHand(uclar, eklemler):
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
                    cv2.putText(
                        frame,
                        "Ellerin havada bekle!",
                        (50, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.1,
                        (0, 0, 255),
                        3,
                )

        else:
            cv2.putText(
                frame,
                "vuruldun",
                (50, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.1,
                (0, 0, 255),
                3,
            )

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


tk.Label(root, text="Adın ne?", font=("Arial", 12)).pack(pady=10)

kutu = tk.Entry(root, font=("Arial", 11))
kutu.pack(pady=5)

tk.Button(root, text="Gönder", command=kontrol).pack(pady=8)

sonuc = tk.Label(root, text="", font=("Arial", 12, "bold"))
sonuc.pack(pady=5)


root.mainloop()
camera.release()
cv2.destroyAllWindows()



