import cv2
import mediapipe as mp
import tkinter as tk

# Sabitler
uclar = [8, 12, 16, 20]
eklemler = [6, 10, 14, 18]
img = cv2.imread("ilkkan.jpeg")

# --- 1. ARAYÜZ (TKINTER) ---
root = tk.Tk()
root.title("Giriş")
root.geometry("350x180+655+440")

# Ekran ölçüsünü sahte pencere açmadan doğrudan root üzerinden alıyoruz
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_merkez = (screen_width - 900) // 2
y_merkez = ((screen_height - 480) // 2) - 150


def Start_Camera():
    root.destroy()  # Tkinter'ı tamamen kapat
    targetHand(uclar, eklemler)  # Kamerayı şimdi başlat


def kontrol():
    cevap = kutu.get().strip().lower()
    if cevap == "rüzgar hasan yaranır":
        btn_gonder.config(state="disabled")  # Tekrar tıklanıp çökertilmesini engelle
        sonuc.config(text="Ellerini kaldır!", fg="red")
        root.after(5000, Start_Camera)
    else:
        sonuc.config(text="GEÇ.", fg="green")


# --- 2. KAMERA VE MEDIAPIPE DÖNGÜSÜ ---
def targetHand(uclar, eklemler):
    # Kamera ve pencere tam bu anda açılıyor
    camera = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

    pencere_konumlandi = False

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

        # Mac ilk kareyi çizdikten sonra pencereyi merkeze oturtuyoruz
        if not pencere_konumlandi:
            cv2.moveWindow("Camera", x_merkez, y_merkez)
            pencere_konumlandi = True

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


# Bileşenler
tk.Label(root, text="Adın ne?", font=("Arial", 12)).pack(pady=10)

kutu = tk.Entry(root, font=("Arial", 11))
kutu.pack(pady=5)

btn_gonder = tk.Button(root, text="Gönder", command=kontrol)
btn_gonder.pack(pady=8)

sonuc = tk.Label(root, text="", font=("Arial", 12, "bold"))
sonuc.pack(pady=5)

root.mainloop()


