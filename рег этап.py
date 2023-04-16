import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk


def start_video():
    cap = cv2.VideoCapture('bobbles.mp4')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    _, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame,
                             cv2.COLOR_BGR2GRAY)  # Преобразует кадр в оттенки серого и сохраняет его в переменной
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray, prev_gray)
        _, thresh = cv2.threshold(diff, 20, 255,
                                  cv2.THRESH_BINARY)  # Применяет пороговую обработку к разнице между текущим и предыдущим кадром
        kernel = np.ones((5, 5), np.uint8)  # создание ядра 5х5 для морфологической операции
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
                                  kernel)  # выполнение морфологической операции закрытия для устранения шума на изображении
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)  # поиск контуров на бинаризованном изображении
        for cnt in contours:
            area = cv2.contourArea(cnt)  # вычисление площади контура
            if area > 500:
                rect = cv2.boundingRect(cnt)
                x, y, w, h = rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        prev_gray = gray.copy()
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def on_start_button_click():
    start_video()


root = tk.Tk()
root.title("Камера видеонаблюдения")
root.geometry("400x200")

title_label = ttk.Label(root, text="Камера видеонаблюдения", font=('Helvetica', 20), foreground='#7289da')
title_label.pack(pady=20)

start_button = ttk.Button(root, text="Запустить", command=on_start_button_click, width=20)
start_button.pack()

exit_button = ttk.Button(root, text="Выход", command=root.destroy, width=20)
exit_button.pack(pady=20)

root.mainloop()