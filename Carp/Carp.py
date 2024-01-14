import cv2
import numpy as np
import pyautogui
import time
import os
import pygetwindow as gw  # Added import for pygetwindow

img_folder_path = os.path.join(os.getcwd(), 'img', 0)

img =cv2.imread(img_folder_path)
cv2.imshow("pala",img)
cv2.waitKey(0)
cv2.destroyAllWindows()





def main():
    # Find the path to the 'Img' folder within the current working directory

    # Check if the 'Img' folder exists
    if not os.path.exists(img_folder_path):
        print(f"Error: Folder {img_folder_path} not found.")
        return

    # Assuming the template image is always named 'hole_template.png'
    template_filename = 'hole_template.png'
    template_path = os.path.join(img_folder_path, template_filename)

    # Check if the template file exists
    if not os.path.exists(template_path):
        print(f"Error: Template file {template_path} not found.")
        return

    full_window_title = "Puzzle Pirates - Yolomaister on the Emerald ocean"
    full_game_window = gw.getWindowsWithTitle(full_window_title)
    window = full_game_window[0]

    if window:
        window.activate()
        print("Window activated.")



if __name__ == "__main__":
    main()
