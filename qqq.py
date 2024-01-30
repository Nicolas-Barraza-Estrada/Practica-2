import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.vid = cv2.VideoCapture(0)

        self.canvas = tk.Canvas(window, width=self.vid.get(3), height=self.vid.get(4))
        self.canvas.pack()

        self.btn_click = ttk.Button(window, text="Click Aqui", command=self.toggle_camera)
        self.btn_click.pack(pady=10)

        self.is_camera_active = True
        self.update()

        self.window.mainloop()

    def toggle_camera(self):
        self.is_camera_active = not self.is_camera_active

    def update(self):
        if self.is_camera_active:
            ret, frame = self.vid.read()
            if ret:
                self.photo = self.convert_frame_to_photo(frame)
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(10, self.update)

    def convert_frame_to_photo(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        return photo

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Inicia la aplicación
root = tk.Tk()
app = App(root, "Cámara con Tkinter y OpenCV")
