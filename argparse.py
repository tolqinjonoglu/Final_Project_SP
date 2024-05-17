import os
import time
import hashlib
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

SOURCE = {}
DESTINATION = {}

def main():
    root = tk.Tk()
    root.title("Folder Synchronizer")

    source_label = tk.Label(root, text="Source Folder:")
    source_label.grid(row=0, column=0, padx=5, pady=5)
    source_entry = tk.Entry(root)
    source_entry.grid(row=0, column=1, padx=5, pady=5)

    destination_label = tk.Label(root, text="Destination Folder:")
    destination_label.grid(row=1, column=0, padx=5, pady=5)
    destination_entry = tk.Entry(root)
    destination_entry.grid(row=1, column=1, padx=5, pady=5)

    interval_label = tk.Label(root, text="Sync Interval (seconds):")
    interval_label.grid(row=2, column=0, padx=5, pady=5)
    interval_entry = tk.Entry(root)
    interval_entry.grid(row=2, column=1, padx=5, pady=5)

    log_label = tk.Label(root, text="Log File (optional):")
    log_label.grid(row=3, column=0, padx=5, pady=5)
    log_entry = tk.Entry(root)
    log_entry.grid(row=3, column=1, padx=5, pady=5)

    start_button = tk.Button(root, text="Start Synchronization", command=lambda: start_sync(source_entry.get(), destination_entry.get(), interval_entry.get(), log_entry.get()))
    start_button.grid(row=4, columnspan=2, padx=5, pady=5)

    root.mainloop()

def start_sync(source, destination, interval, log):
    if not os.path.exists(source):
        messagebox.showerror("Error", "Source folder does not exist.")
        return
    if not os.path.exists(destination):
        messagebox.showerror("Error", "Destination folder does not exist.")
        return

    try:
        interval = int(interval)
        if interval <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Interval must be a positive integer.")
        return

    try:
        while True:
            synchronize(source, destination, log)
            time.sleep(interval)
    except KeyboardInterrupt:
        pass

def read_file(path):
    with open(path, 'rb') as f:
        return f.read()

def write_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)

def append_file(path, data):
    with open(path, 'a') as f:
        msg = str(datetime.now()) + ' [info] ' + data + '\n'
        f.write(msg)

def copy_file(source_file_path, destination_file_path):
    write_file(destination_file_path, read_file(source_file_path))

def update_record(source, destination):
    global SOURCE
    global DESTINATION
    SOURCE = {}
    DESTINATION = {}
    for root, _, files in os.walk(source):
        directory = root[len(source):].lstrip(os.sep)
        if directory:
            SOURCE[directory] = hashlib.md5(directory.encode()).hexdigest()
        for file in files:
            file_path = os.path.join(directory, file)
            SOURCE[file_path] = hashlib.md5(read_file(os.path.join(root, file))).hexdigest()

    for root, _, files in os.walk(destination):
        directory = root[len(destination):].lstrip(os.sep)
        if directory:
            DESTINATION[directory] = hashlib.md5(directory.encode()).hexdigest()
        for file in files:
            file_path = os.path.join(directory, file)
            DESTINATION[file_path] = hashlib.md5(read_file(os.path.join(root, file))).hexdigest()

def synchronize(source, destination, log):
    update_record(source, destination)
    changes_made = False

    for key, val in SOURCE.items():
        s = os.path.join(source, key)
        d = os.path.join(destination, key)
        if DESTINATION.get(key) is None or DESTINATION[key] != SOURCE[key]:
            changes_made = True
            if os.path.isdir(s):
                if not os.path.exists(d):
                    os.makedirs(d)
                    md_msg = f"Created folder {key} in {destination}"
                    if log:
                        append_file(log, md_msg)
                    print(md_msg)
            else:
                copy_file(s, d)
                cpy_msg = f"Copied file {key} to {destination}"
                if log:
                    append_file(log, cpy_msg)
                print(cpy_msg)
            DESTINATION[key] = val

    for key in list(sorted(DESTINATION, reverse=True)):
        s = os.path.join(source, key)
        d = os.path.join(destination, key)
        if SOURCE.get(key) is None:
            changes_made = True
            if os.path.isdir(d):
                os.rmdir(d)
                rm_msg = f"Removed folder {key} from {destination}"
                if log:
                    append_file(log, rm_msg)
                print(rm_msg)
            elif os.path.isfile(d):
                os.remove(d)
                rm_file = f"Removed file {key} from {destination}"
                if log:
                    append_file(log, rm_file)
                print(rm_file)
            DESTINATION.pop(key, None)

    if not changes_made:
        print("Synchronized")

if __name__ == '__main__':
    main()