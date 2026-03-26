import pyautogui
import time

print("Move your mouse to the video call button (camera icon) in WhatsApp")
print("You have 5 seconds...")
time.sleep(5)

x, y = pyautogui.position()
print(f"Video call button coordinates: x={x}, y={y}")