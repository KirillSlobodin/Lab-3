import os
import random
import string
import subprocess
import sys
import tkinter as tk

print("[1/4] Скрипт запущен...")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BLOCK_COUNT = 3
BLOCK_LENGTH = 4
MIN_WEIGHT = 30
MAX_WEIGHT = 35

WEIGHTS = {letter: idx + 1 for idx, letter in enumerate(string.ascii_uppercase)}
for digit in string.digits:
    WEIGHTS[digit] = int(digit)

ALPHABET = list(WEIGHTS.keys())


def generate_block() -> tuple[str, int]:
    while True:
        chars = random.choices(ALPHABET, k=BLOCK_LENGTH)
        total_weight = sum(WEIGHTS[ch] for ch in chars)
        if MIN_WEIGHT <= total_weight <= MAX_WEIGHT:
            return "".join(chars), total_weight


def generate_full_key() -> tuple[str, list[int]]:
    blocks, sums = [], []
    for _ in range(BLOCK_COUNT):
        block, block_sum = generate_block()
        blocks.append(block)
        sums.append(block_sum)
    return "-".join(blocks), sums


class KeygenApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Cyberpunk 2077 — Keygen [Variant 4]")
        self.root.geometry("600x380")
        self.root.resizable(False, False)

        # Принудительно поднимаем окно поверх всех окон на macOS
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after(200, lambda: self.root.attributes("-topmost", False))
        self.root.focus_force()

        self.music_proc = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.canvas = tk.Canvas(root, width=600, height=380, bg="#0D0D12", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.bg_image = None
        bg_path = os.path.join(BASE_DIR, "bg.png")
        if os.path.exists(bg_path):
            try:
                self.bg_image = tk.PhotoImage(file=bg_path)
                self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
                print("[INFO] Фоновая картинка bg.png загружена.")
            except tk.TclError as e:
                print(f"[WARN] Не удалось прочитать bg.png (нужен настоящий PNG): {e}")
        else:
            print("[INFO] Файл bg.png не найден, используется стандартный фон.")

        self.particles = [
            {
                "id": self.canvas.create_oval(x, y, x + 3, y + 3, fill="#00F0FF", outline=""),
                "speed": random.uniform(1.0, 3.0)
            }
            for x, y in ((random.randint(10, 590), random.randint(10, 370)) for _ in range(35))
        ]

        self.canvas.create_text(
            300, 65,
            text="CYBERPUNK 2077 KEYGEN",
            font=("Courier", 24, "bold"),
            fill="#FCEE09"
        )

        self.key_var = tk.StringVar(value="XXXX-XXXX-XXXX")
        self.key_entry = tk.Entry(
            root,
            textvariable=self.key_var,
            font=("Courier", 20, "bold"),
            justify="center",
            bg="#1A1A24",
            fg="#00F0FF",
            bd=2,
            relief="flat",
            readonlybackground="#1A1A24",
            state="readonly"
        )
        self.canvas.create_window(300, 175, window=self.key_entry, width=340, height=45)

        self.sums_text_id = self.canvas.create_text(
            300, 225,
            text=f"Интервал весов блока: {MIN_WEIGHT}..{MAX_WEIGHT}",
            font=("Courier", 12),
            fill="#FFFFFF"
        )

        self.gen_button = tk.Button(
            root,
            text="GENERATE KEY",
            font=("Courier", 14, "bold"),
            bg="#FCEE09",
            fg="#0D0D12",
            activebackground="#00F0FF",
            activeforeground="#0D0D12",
            cursor="hand2",
            command=self.on_generate_click
        )
        self.canvas.create_window(300, 290, window=self.gen_button, width=220, height=45)

        self.keep_music_playing()
        self.animate()
        print("[3/4] Интерфейс отрисован, окно должно быть на экране!")

    def keep_music_playing(self):
        music_path = os.path.join(BASE_DIR, "music.mp3")
        if sys.platform == "darwin" and os.path.exists(music_path):
            if self.music_proc is None or self.music_proc.poll() is not None:
                self.music_proc = subprocess.Popen(
                    ["afplay", music_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
        self.root.after(1000, self.keep_music_playing)

    def on_close(self):
        if self.music_proc and self.music_proc.poll() is None:
            self.music_proc.terminate()
        self.root.destroy()

    def on_generate_click(self):
        self.gen_button.config(state="disabled")
        self.shuffle_step(0)

    def shuffle_step(self, step: int):
        if step < 8:
            fake_blocks = [
                "".join(random.choices(ALPHABET, k=BLOCK_LENGTH))
                for _ in range(BLOCK_COUNT)
            ]
            self.key_var.set("-".join(fake_blocks))
            self.root.after(40, self.shuffle_step, step + 1)
        else:
            final_key, sums = generate_full_key()
            self.key_var.set(final_key)
            sums_str = "-".join(map(str, sums))
            self.canvas.itemconfig(
                self.sums_text_id,
                text=f"Суммы весов: {sums_str} (норма {MIN_WEIGHT}..{MAX_WEIGHT})"
            )
            self.gen_button.config(state="normal")

    def animate(self):
        for p in self.particles:
            self.canvas.move(p["id"], 0, p["speed"])
            coords = self.canvas.coords(p["id"])
            if coords and coords[1] > 380:
                new_x = random.randint(10, 590)
                self.canvas.coords(p["id"], new_x, -5, new_x + 3, -2)
        self.root.after(30, self.animate)


print("[2/4] Создаём окно Tkinter...")
root = tk.Tk()
app = KeygenApp(root)
print("[4/4] Запуск главного цикла (mainloop)...")
root.mainloop()