# import tkinter as tk
# from tkinter import messagebox
# import time

# class PomodoroTimer:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Pomodoro Timer")

#         self.work_time = 25 * 60  # 25 minutes work time in seconds
#         self.break_time = 5 * 60  # 5 minutes break time in seconds
#         self.current_time = self.work_time
#         self.timer_running = False

#         self.label = tk.Label(master, text="00:00", font=("Helvetica", 48))
#         self.label.pack(pady=20)

#         self.start_button = tk.Button(master, text="Start", command=self.start_timer)
#         self.start_button.pack(side=tk.LEFT, padx=10)

#         self.stop_button = tk.Button(master, text="Stop", command=self.stop_timer)
#         self.stop_button.pack(side=tk.LEFT, padx=10)

#         self.reset_button = tk.Button(master, text="Reset", command=self.reset_timer)
#         self.reset_button.pack(side=tk.LEFT, padx=10)

#         self.work_time_label = tk.Label(master, text="Work Time (min):")
#         self.work_time_label.pack(side=tk.LEFT, padx=10)
#         self.work_time_entry = tk.Entry(master, width=5)
#         self.work_time_entry.insert(tk.END, "25")
#         self.work_time_entry.pack(side=tk.LEFT)

#         self.break_time_label = tk.Label(master, text="Break Time (min):")
#         self.break_time_label.pack(side=tk.LEFT, padx=10)
#         self.break_time_entry = tk.Entry(master, width=5)
#         self.break_time_entry.insert(tk.END, "5")
#         self.break_time_entry.pack(side=tk.LEFT)

#     def start_timer(self):
#         if not self.timer_running:
#             self.timer_running = True
#             self.work_time = int(self.work_time_entry.get()) * 60
#             self.break_time = int(self.break_time_entry.get()) * 60
#             self.current_time = self.work_time
#             self.count_down()

#     def stop_timer(self):
#         if self.timer_running:
#             self.timer_running = False
#             messagebox.showinfo("Pomodoro Timer", "Timer stopped")

#     def reset_timer(self):
#         self.timer_running = False
#         self.current_time = self.work_time
#         self.label.config(text="00:00")

#     def count_down(self):
#         minutes, seconds = divmod(self.current_time, 60)
#         self.label.config(text=f"{minutes:02d}:{seconds:02d}")
#         if self.current_time > 0 and self.timer_running:
#             self.current_time -= 1
#             self.master.after(1000, self.count_down)
#         elif self.current_time == 0:
#             messagebox.showinfo("Pomodoro Timer", "Time's up!")
#             self.timer_running = False
#             self.after_break()

#     def after_break(self):
#         if messagebox.askyesno("Pomodoro Timer", "Take a break?"):
#             self.current_time = self.break_time
#             self.count_down()
#         else:
#             self.reset_timer()

# def main():
#     root = tk.Tk()
#     pomodoro_timer = PomodoroTimer(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()
