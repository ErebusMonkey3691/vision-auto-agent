import pyautogui
import win32gui
import win32con
from PIL import Image
import time
import keyboard
import threading
import sys

og_pos = pyautogui.position()

hwnd = win32gui.FindWindow(None, "GameWindow")
if not hwnd:
    raise Exception("Window not found!")

win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
win32gui.SetWindowPos(hwnd, None, 0, 0, 800, 600, win32con.SWP_NOZORDER)

left, top, right, bottom = win32gui.GetWindowRect(hwnd)
width = right - left
height = bottom - top
print(f"Window coordinates: {left},{top} -> {right},{bottom}")

reference_button = Image.open("reference_button.png")
confirm_button = Image.open("reference_confirm.png")

# Compute average color of given image
def average_color(img):
    pixels = img.getdata()
    num_pixels = len(pixels)
    r = sum(p[0] for p in pixels) / num_pixels
    g = sum(p[1] for p in pixels) / num_pixels
    b = sum(p[2] for p in pixels) / num_pixels
    return (r, g, b)



# Kill switch: stop script if "ESC" is pressed
def kill_switch():
    keyboard.wait("esc")
    print("\nKill switch triggered! Exiting...")
    sys.exit(0)

# Start kill switch in a separate thread
threading.Thread(target=kill_switch, daemon=True).start()

def one_step():
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot.save("window_capture.png")  # optional: save it to see what it looks like

    button_region = (616, 481, 628, 491)  # (left, top, right, bottom) relative to window
    button_img = screenshot.crop(button_region)
    button_img.save("button_image.png")  # optional: see what the cropped area looks like
    offset_x = 23
    button_region = (offset_x + 616, 481, offset_x + 628, 491)
    button_img2 = screenshot.crop(button_region)



    confirm_region = (645, 423, 732, 442)
    confirm_img = screenshot.crop(confirm_region)
    confirm_img.save("confirm_image.png")

    avg_screenshot = average_color(button_img)
    avg_reference = average_color(reference_button)

    print(f"Screenshot avg color: {avg_screenshot}")
    print(f"Reference avg color: {avg_reference}")

    # Is button present?
    threshold = 5  # max difference per channel
    if all(abs(a - b) < threshold for a, b in zip(avg_screenshot, avg_reference)):
        print("Button is present!")
        # Click button
        winRate_x, winRate_y = 603, 484  # Win rate up button
        start_x, start_y = 540, 490  # Start button
        pyautogui.moveTo(winRate_x, winRate_y)
        pyautogui.click()
        pyautogui.moveTo(start_x, start_y)
        pyautogui.click()
    else:
        print("Button not detected.")
        avg_screenshot = average_color(button_img2)
        if all(abs(a - b) < threshold for a, b in zip(avg_screenshot, avg_reference)):
            print("Button2 is present!")
            winRate_x, winRate_y = 603+offset_x, 484  # Win rate up button
            start_x, start_y = 540+offset_x, 490  # Start button
            pyautogui.moveTo(winRate_x, winRate_y)
            pyautogui.click()
            pyautogui.moveTo(start_x, start_y)
            pyautogui.click()
        else:
            avg_screenshot = average_color(confirm_img)
            avg_reference = average_color(confirm_button)
            print(f"Screenshot avg color: {avg_screenshot}")
            print(f"Reference avg color: {avg_reference}")
            if all(abs(a - b) < threshold for a, b in zip(avg_screenshot, avg_reference)):
                print("Confirm button is present! Combat complete.")
                # Click confirm
                # Break out of loop :p
                confirm_x, confirm_y = 685, 432
                pyautogui.moveTo(confirm_x, confirm_y)
                pyautogui.click()
                return 0
    return 1
        # Check if confirm button is detected.

lastStep = 1

while lastStep:
    lastStep = one_step()
    time.sleep(1)
    print(f"Last step returned: {lastStep}")

print("Moving mouse back to starting position :p")
pyautogui.moveTo(og_pos)
