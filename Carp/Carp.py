import cv2
import numpy as np
import pyautogui
import time
import os

def find_hole(template_path):
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)

    # Read the template image
    template = cv2.imread(template_path)

    # Convert the images to grayscale
    gray_screenshot = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Match the template in the screenshot
    result = cv2.matchTemplate(gray_screenshot, gray_template, cv2.TM_CCOEFF_NORMED)

    # Define a threshold to consider a match
    threshold = 0.8
    loc = np.where(result >= threshold)

    if loc[0].size > 0:
        # At least one match found
        return True
    else:
        return False

def main():
    # Find the path to the 'Img' folder within the current working directory
    img_folder_path = os.path.join(os.getcwd(), 'Img')

    # Assuming the template image is always named 'hole_template.png'
    template_filename = 'hole_template.png'
    template_path = os.path.join(img_folder_path, template_filename)

    full_window_title = "Puzzle Pirates - Urbanman on the Emerald ocean"
    full_game_window = gw.getWindowsWithTitle(full_window_title)
    window = full_game_window[0]

    if window:
        window.activate()
        print("Starting bot...")

        time.sleep(2)  # Give some time for the window to be active

        if find_hole(template_path):
            print("Hole found!")
        else:
            print("Hole not found.")

if __name__ == "__main__":
    main()
