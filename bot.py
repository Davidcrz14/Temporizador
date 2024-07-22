import tkinter as tk
from tkinter import messagebox
import math
import winsound

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DavC's Timer")
        self.root.geometry("500x600")
        self.root.config(bg="#F3E5F5")

        self.time_left = 0
        self.running = False

        self.setup_ui()
        self.setup_clock()

    def setup_ui(self):
        title_font = ("Helvetica", 24, "bold")
        label_font = ("Helvetica", 18)
        button_font = ("Helvetica", 16)

        tk.Label(self.root, text="DavC's Timer", font=title_font, bg="#F3E5F5", fg="#673AB7").pack(pady=20)

        self.time_display = tk.Label(self.root, text="00:00:00", font=("Helvetica", 48), bg="#F3E5F5", fg="#673AB7")
        self.time_display.pack(pady=20)

        input_frame = tk.Frame(self.root, bg="#F3E5F5")
        input_frame.pack(pady=20)

        labels = ["Horas:", "Minutos:", "Segundos:"]
        self.time_entries = []

        for label in labels:
            tk.Label(input_frame, text=label, font=label_font, bg="#F3E5F5", fg="#673AB7").pack(side=tk.LEFT, padx=5)
            entry = tk.Entry(input_frame, font=label_font, width=3, bg="#E1BEE7", fg="#673AB7", insertbackground="#673AB7")
            entry.pack(side=tk.LEFT, padx=5)
            self.time_entries.append(entry)

        button_frame = tk.Frame(self.root, bg="#F3E5F5")
        button_frame.pack(pady=20)

        self.start_button = tk.Button(button_frame, text="INICIAR", command=self.toggle_timer, font=button_font, bg="#BA68C8", fg="#FFFFFF", activebackground="#AB47BC", activeforeground="#FFFFFF")
        self.start_button.pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="REINICIAR", command=self.reset_timer, font=button_font, bg="#F48FB1", fg="#FFFFFF", activebackground="#F06292", activeforeground="#FFFFFF").pack(side=tk.LEFT, padx=10)

    def setup_clock(self):
        self.canvas = tk.Canvas(self.root, width=200, height=200, bg="#F3E5F5", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.draw_clock_face()
        self.update_clock_hands()

    def draw_clock_face(self):
        self.canvas.create_oval(10, 10, 190, 190, outline="#673AB7", width=2)

        for i in range(12):
            angle = i * math.pi / 6 - math.pi / 2
            x1 = 100 + 80 * math.cos(angle)
            y1 = 100 + 80 * math.sin(angle)
            x2 = 100 + 90 * math.cos(angle)
            y2 = 100 + 90 * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2, fill="#673AB7", width=2)

    def update_clock_hands(self):
        self.canvas.delete("hand")

        total_seconds = self.time_left
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        hour_angle = (hours % 12 + minutes / 60) * math.pi / 6 - math.pi / 2
        self.draw_hand(hour_angle, 50, 6, "#D32F2F")

        minute_angle = (minutes + seconds / 60) * math.pi / 30 - math.pi / 2
        self.draw_hand(minute_angle, 70, 4, "#388E3C")

        second_angle = seconds * math.pi / 30 - math.pi / 2
        self.draw_hand(second_angle, 80, 2, "#1976D2")

        self.root.after(1000, self.update_clock_hands)

    def draw_hand(self, angle, length, width, color):
        x = 100 + length * math.cos(angle)
        y = 100 + length * math.sin(angle)
        self.canvas.create_line(100, 100, x, y, fill=color, width=width, tags="hand")

    def toggle_timer(self):
        if self.running:
            self.running = False
            self.start_button.config(text="INICIAR", bg="#BA68C8", activebackground="#AB47BC")
        else:
            try:
                hours = int(self.time_entries[0].get() or 0)
                minutes = int(self.time_entries[1].get() or 0)
                seconds = int(self.time_entries[2].get() or 0)
                self.time_left = hours * 3600 + minutes * 60 + seconds
                if self.time_left > 0:
                    self.running = True
                    self.start_button.config(text="PAUSAR", bg="#FFB300", activebackground="#FFA000")
                    self.update_timer()
                else:
                    messagebox.showerror("Error", "Por favor, introduce un tiempo válido.")
            except ValueError:
                messagebox.showerror("Error", "Por favor, introduce valores numéricos válidos.")

    def update_timer(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.update_display()
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.running = False
            self.start_button.config(text="INICIAR", bg="#BA68C8", activebackground="#AB47BC")
            self.play_sound()
            messagebox.showinfo("Tiempo finalizado", "¡El tiempo ha terminado!")

    def update_display(self):
        hours, remainder = divmod(self.time_left, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_format = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.time_display.config(text=time_format)

    def reset_timer(self):
        self.running = False
        self.time_left = 0
        self.update_display()
        self.start_button.config(text="INICIAR", bg="#BA68C8", activebackground="#AB47BC")
        for entry in self.time_entries:
            entry.delete(0, tk.END)

    def play_sound(self):
        try:
           winsound.Beep(1000, 1000)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo reproducir el sonido: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
