import ctypes
import win32gui
import win32ui
import win32con
import os

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

def capture_window(window_title, output_file="capture.bmp"):
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        raise Exception(f"Window '{window_title}' not found.")

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)

    # Use ctypes to call PrintWindow
    PW_RENDERFULLCONTENT = 0x00000002  # optional flag
    result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), PW_RENDERFULLCONTENT)

    if result == 1:
        save_bitmap.SaveBitmapFile(save_dc, output_file)
        print(f"Saved screenshot to {output_file}")
        os.startfile(output_file)  # open automatically
    else:
        print("Failed to capture window. Might be minimized or not renderable.")

    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

# Example usage
capture_window("GameWindow", "GameWindow.bmp")
