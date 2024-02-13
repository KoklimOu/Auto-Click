from pynput.mouse import Listener, Button
import pyautogui
import threading
import tkinter as tk
import time
import os

# Specify the correct path to the generated executable file
executable_path = '/home/cosetto/Documents/auto_click/dist/auto_click3'

desktop_entry = f"""
[Desktop Entry]
Name=Auto Click V3
Exec={executable_path}
Type=Application
Terminal=false
"""

desktop_path = os.path.expanduser("~/.local/share/applications/auto_click3.desktop")

with open(desktop_path, "w") as desktop_file:
    desktop_file.write(desktop_entry)

target_coordinates = None
start_time = None
auto_clicking = False  # Variable to track the state of auto-clicking

def on_click(x, y, button, pressed):
    global target_coordinates, start_time

    if pressed and button == Button.right:
        target_coordinates = (x, y)
        start_time = time.time()
        update_ui()

def toggle_auto_click():
    global auto_clicking

    if auto_clicking:
        auto_clicking = False
        status_label_var.set("Auto-Click Stopped")
    else:
        auto_clicking = True
        start_auto_click_loop()

def start_auto_click_loop():
    global target_coordinates, start_time
    if target_coordinates:
        status_label_var.set("Auto-Click Started")
        threading.Thread(target=auto_click_loop, args=(target_coordinates[0], target_coordinates[1]), daemon=True).start()
        # Schedule the update_ui function to run every 100 milliseconds
        root.after(100, update_ui)

def auto_click_loop(target_x, target_y):
    while auto_clicking:
        pyautogui.click(target_x, target_y)
        # Add sleep duration as needed
        time.sleep(0.5)

def update_ui():
    if target_coordinates and auto_clicking:
        x, y = target_coordinates
        current_time = time.time() - start_time if start_time else 0

        # Update the coordinate label
        coordinates_label_var.set(f"Target Coordinates: ({x}, {y})")

        # Update the time label
        time_label_var.set(f"Time Running: {current_time:.2f} seconds")

        # Schedule the update_ui function to run again after 100 milliseconds
        root.after(100, update_ui)

def cancel_application():
    root.destroy()  # Destroy the Tkinter window, effectively closing the application

# Create the main window
root = tk.Tk()
root.title("Auto-Click Start")

# Set window attributes
root.overrideredirect(True)  # Remove window decorations (title bar, etc.)
root.attributes("-topmost", True)  # Bring the window to the front

# Move the window to a specific position on the screen (adjust coordinates as needed)
root.geometry("+100+100")

# Create UI elements
start_button = tk.Button(root, text="Toggle Auto-Click", command=toggle_auto_click)
start_button.pack(pady=10)

status_label_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_label_var)
status_label.pack()

coordinates_label_var = tk.StringVar()
coordinates_label = tk.Label(root, textvariable=coordinates_label_var)
coordinates_label.pack()

time_label_var = tk.StringVar()
time_label = tk.Label(root, textvariable=time_label_var)
time_label.pack()

# Add Cancel Button
cancel_button = tk.Button(root, text="Cancel", command=cancel_application)
cancel_button.pack()

# Set up the mouse listener
with Listener(on_click=on_click) as listener:
    root.mainloop()
