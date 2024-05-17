# import tkinter as tk
# from tkinter import messagebox
# import os
# import time
# import hashlib
# from datetime import datetime

# SOURCE = {}
# DESTINATION = {}

# def main():
#     root = tk.Tk()
#     root.title("Folder Synchronizer")

#     # Source folder entry
#     source_frame = tk.Frame(root)
#     source_frame.pack(pady=10)
#     source_label = tk.Label(source_frame, text="Source Folder:")
#     source_label.pack(side=tk.LEFT, padx=5)
#     source_entry = tk.Entry(source_frame, width=50)
#     source_entry.pack(side=tk.LEFT, padx=5)

#     # Destination folder entry
#     dest_frame = tk.Frame(root)
#     dest_frame.pack(pady=10)
#     dest_label = tk.Label(dest_frame, text="Destination Folder:")
#     dest_label.pack(side=tk.LEFT, padx=5)
#     dest_entry = tk.Entry(dest_frame, width=50)
#     dest_entry.pack(side=tk.LEFT, padx=5)

#     # Interval entry
#     interval_frame = tk.Frame(root)
#     interval_frame.pack(pady=10)
#     interval_label = tk.Label(interval_frame, text="Sync Interval (seconds):")
#     interval_label.pack(side=tk.LEFT, padx=5)
#     interval_entry = tk.Entry(interval_frame, width=10)
#     interval_entry.pack(side=tk.LEFT, padx=5)

#     # Log file entry
#     log_frame = tk.Frame(root)
#     log_frame.pack(pady=10)
#     log_label = tk.Label(log_frame, text="Log File (optional):")
#     log_label.pack(side=tk.LEFT, padx=5)
#     log_entry = tk.Entry(log_frame, width=50)
#     log_entry.pack(side=tk.LEFT, padx=5)

#     # Start synchronization button
#     def start_sync():
#         source = source_entry.get()
#         dest = dest_entry.get()
#         interval = interval_entry.get()
#         log = log_entry.get()
#         if not source or not dest or not interval:
#             messagebox.showerror("Error", "Please fill in all required fields.")
#             return
#         try:
#             interval = int(interval)
#             if interval <= 0:
#                 raise ValueError
#         except ValueError:
#             messagebox.showerror("Error", "Sync Interval must be a positive integer.")
#             return
#         status_label.config(text="Synchronizing...", fg="blue")
#         synchronize(source, dest, log, interval, status_label)

#     start_button = tk.Button(root, text="Start Synchronization", command=start_sync)
#     start_button.pack(pady=10)

#     # Status label
#     status_label = tk.Label(root, text="", fg="green")
#     status_label.pack(pady=5)

#     root.mainloop()

# def synchronize(source, destination, log, interval, status_label):
#     try:
#         while True:
#             update_record(source, destination)
#             if SOURCE == DESTINATION:
#                 status_label.config(text="Synchronized", fg="green")
#             else:
#                 for key, val in SOURCE.items():
#                     s = os.path.join(source, key)
#                     d = os.path.join(destination, key)
#                     if DESTINATION.get(key) is None or DESTINATION[key] != SOURCE[key]:
#                         if os.path.isdir(s):
#                             if not os.path.exists(d):
#                                 os.makedirs(d)
#                                 if log:
#                                     append_file(log, f"Creating folder {key} in {d}")
#                             print(f"Creating folder {key} in {d}")
#                         else:
#                             copy_file(s, d)
#                             if log:
#                                 append_file(log, f"Copying file {key} to {d}")
#                             print(f"Copying file {key} to {d}")
#                     DESTINATION[key] = val

#                 for key in list(sorted(DESTINATION, reverse=True)):
#                     s = os.path.join(source, key)
#                     d = os.path.join(destination, key)
#                     if SOURCE.get(key) is None:
#                         if os.path.isdir(d):
#                             os.rmdir(d)
#                             if log:
#                                 append_file(log, f"Removing folder {key} from {d}")
#                             print(f"Removing folder {key} from {d}")
#                         if os.path.isfile(d):
#                             os.remove(d)
#                             if log:
#                                 append_file(log, f"Removing file {key} from {d}")
#                             print(f"Removing file {key} from {d}")
#                         DESTINATION.pop(key, None)
#             time.sleep(interval)
#     except KeyboardInterrupt:
#         status_label.config(text="Synchronization Stopped", fg="red")

# def read_file(path):
#     with open(path, 'rb') as f:
#         return f.read()

# def write_file(path, data):
#     with open(path, 'wb') as f:
#         f.write(data)

# def append_file(path, data):
#     with open(path, 'a') as f:
#         msg = str(datetime.now()) + ' [info] ' + data + '\n'
#         f.write(msg)

# def copy_file(source_file_path, destination_file_path):
#     write_file(destination_file_path, read_file(source_file_path))

# def update_record(source, destination):
#     global SOURCE
#     global DESTINATION
#     SOURCE = {}
#     DESTINATION = {}
#     for root, _, files in os.walk(source):
#         directory = root.split(source)[1][1:]
#         if len(directory) > 1:
#             SOURCE[directory] = hashlib.md5(directory.encode()).hexdigest()
#         for file in files:
#             SOURCE[os.path.join(directory, file)] = hashlib.md5(read_file(os.path.join(root, file))).hexdigest()

#     for root, _, files in os.walk(destination):
#         directory = root.split(destination)[1][1:]
#         if len(directory) > 1:
#             DESTINATION[directory] = hashlib.md5(directory.encode()).hexdigest()
#         for file in files:
#             DESTINATION[os.path.join(directory, file)] = hashlib.md5(read_file(os.path.join(root, file))).hexdigest()

# if __name__ == '__main__':
#     main()