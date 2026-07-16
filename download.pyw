import tkinter as tk
import random
from PIL import Image, ImageTk
import pygame
import os

# Create folder in LocalAppData
base = os.path.join(os.getenv("LOCALAPPDATA"), "无信号")
os.makedirs(base, exist_ok=True)

# Load files from LocalAppData
IMAGE_PATH = os.path.join(base, "photo.png")
MUSIC_PATH = os.path.join(base, "music.mp3")

pygame.mixer.init()

def make_window():
    win = tk.Toplevel() if tk._default_root else tk.Tk()
    win.title("无信号")
    win.geometry("400x300")

    base_img = Image.open(IMAGE_PATH)

    label = tk.Label(win)
    label.pack(expand=True, fill="both")

    sound = pygame.mixer.Sound(MUSIC_PATH)
    sound.play(loops=-1)

    x = random.randint(0, 500)
    y = random.randint(0, 500)
    dx, dy = 3, 3

    update_id = None
    bounce_id = None

    def update_image():
        nonlocal update_id
        if not win.winfo_exists():
            return

        w = win.winfo_width()
        h = win.winfo_height()

        if w > 50 and h > 50:
            resized = base_img.resize((w, h), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(resized)
            label.config(image=tk_img)
            label.image = tk_img

        update_id = win.after(30, update_image)

    def bounce():
        nonlocal x, y, dx, dy, bounce_id
        if not win.winfo_exists():
            return

        x += dx
        y += dy

        if x <= 0 or x + win.winfo_width() >= win.winfo_screenwidth():
            dx = -dx
        if y <= 0 or y + win.winfo_height() >= win.winfo_screenheight():
            dy = -dy

        win.geometry(f"+{x}+{y}")
        bounce_id = win.after(10, bounce)

    def on_close():
        try:
            if update_id:
                win.after_cancel(update_id)
            if bounce_id:
                win.after_cancel(bounce_id)
        except:
            pass

        for _ in range(3):
            make_window()

    win.protocol("WM_DELETE_WINDOW", on_close)

    update_image()
    bounce()

    win.mainloop()

make_window()
