from pynput.mouse import Listener, Button
import pyautogui
import time
import threading

clicks = []
auto_click_active = False

def on_click(x, y, button, pressed):
    """
    Callback function for mouse click events.
    """
    global clicks, auto_click_active

    if pressed and button == Button.right:
        clicks.append((x, y))
        
        if len(clicks) == 2:
            double_click()

def double_click():
    """
    Handle double-click logic.
    """
    global clicks, auto_click_active

    if len(clicks) == 2:
        x1, y1 = clicks[0]
        x2, y2 = clicks[1]

        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        print(distance)
        if distance < 5:
            auto_click_active = not auto_click_active
            print(f"Auto-click {'enabled' if auto_click_active else 'disabled'}")

            if auto_click_active:
                target_x, target_y = clicks[1]
                print(target_x, target_y)
                threading.Thread(target=auto_click_loop, args=(target_x, target_y), daemon=True).start()

            # Clear clicks list
            clicks = []

def auto_click_loop(target_x, target_y):
    """
    Auto-click loop running in a separate thread
    """
    global auto_click_active

    while auto_click_active:
        pyautogui.click(target_x, target_y)
        time.sleep(3)

def main():
    with Listener(on_click=on_click) as listener:
        listener.join()

if __name__ == "__main__":
    main()
