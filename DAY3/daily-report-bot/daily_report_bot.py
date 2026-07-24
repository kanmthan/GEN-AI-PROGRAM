import pyautogui
import pyperclip
import subprocess
import time
from datetime import datetime

pyautogui.FAILSAFE = True

# Current date and time
now = datetime.now()
current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
current_date = now.strftime("%Y-%m-%d")

comment = "Good for outdoor activities"

# -------------------------
# Open Chrome
# -------------------------
subprocess.run(["open", "-a", "Google Chrome"])
time.sleep(3)

# Open weather page
pyautogui.hotkey("command", "l")
time.sleep(1)

pyautogui.write("https://www.google.com/search?q=weather")
pyautogui.press("enter")

time.sleep(5)

# NOTE:
# Manually select the temperature location on your screen.
# Replace x,y with your own coordinates.

pyautogui.doubleClick(x=600, y=350)
pyautogui.hotkey("command", "c")

time.sleep(1)

weather = pyperclip.paste()

# -------------------------
# Open Numbers
# -------------------------
subprocess.run(["open", "-a", "Numbers"])
time.sleep(5)

# Click first empty cell
pyautogui.click(x=300, y=220)

pyautogui.write(current_datetime)
pyautogui.press("tab")

pyautogui.write(weather)
pyautogui.press("tab")

pyautogui.write(comment)

time.sleep(2)

# Screenshot
screenshot_name = f"daily_report_{current_date}.png"
pyautogui.screenshot(screenshot_name)

print("Automation completed.")