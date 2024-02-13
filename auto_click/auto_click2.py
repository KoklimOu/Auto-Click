from pynput.mouse import Listener, Button
import pyautogui
import threading
import tkinter as tk
import time 
import os

# Specify the correct path to the generated executable file
executable_path = '/home/cosetto/Documents/auto_click/dist/auto_click2'

desktop_entry = f"""
[Desktop Entry]
Name=Auto Click
Exec={executable_path}
Type=Application
Terminal=false
"""

desktop_path = os.path.expanduser("~/.local/share/applications/auto_click.desktop")

with open(desktop_path, "w") as desktop_file:
    desktop_file.write(desktop_entry)

target_coordinates = None

def on_click(x, y, button, pressed):
    """
    Callback function for mouse click events.
    """
    global target_coordinates

    if pressed and button == Button.right:
        target_coordinates = (x, y)
        update_ui()

def start_auto_click_loop():
    """
    Start auto-click loop.
    """
    global target_coordinates
    if target_coordinates:
        threading.Thread(target=auto_click_loop, args=(target_coordinates[0], target_coordinates[1]), daemon=True).start()

def auto_click_loop(target_x, target_y):
    """
    Auto-click loop running in a separate thread.
    """
    while True:  # Run indefinitely, you can add a condition to stop the loop
        pyautogui.click(target_x, target_y)
        # Adjust sleep duration as needed
        time.sleep(0.5)

def update_ui():
    """
    Update UI based on target coordinates.
    """
    if target_coordinates:
        x, y = target_coordinates
        print(f"Target Coordinates: ({x}, {y})")

# Create the main window
root = tk.Tk()
root.title("Auto-Click Start")

# Create UI elements
start_button = tk.Button(root, text="Start Auto-Click", command=start_auto_click_loop)
start_button.pack(pady=10)

# Set up the mouse listener
with Listener(on_click=on_click) as listener:
    # Start the UI main loop
    root.mainloop()