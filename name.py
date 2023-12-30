import pygetwindow as gw
import pyautogui
import time
import jotain
import keyboard
import sys

RESET = '\033[0m'
BLUE = '\033[34m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_CYAN = '\033[96m'
GREEN = '\033[32m'
CYAN = '\033[36m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_WHITE = '\033[97m'
BRIGHT_YELLOW = '\033[93m'
BG_MAGENTA = '\033[45m'

STOP_FLAG = False

gamestate : list[list[int]] = []

def print_colored_text(text, color_code):
    return
    print(f"{color_code}{text}{RESET}", end=" ")

def create_empty_array(xsize: int, ysize: int) -> list[list[int]]:

    # Create a 2D array with zeros using lists
    two_d_array = [[0 for _ in range(xsize)] for _ in range(ysize)]

    return two_d_array

def get_gameboard_top_left(window):
    left, top = window.left, window.top
    offset_x = 90 + 3
    offset_y = 77
    return left+offset_x, top+offset_y

def get_piece_coordinate(window, right_amount_blocks,down_amount_blocks): # Start From First Object
    left, top = window.left, window.top
    offset_x = 90 + 3 + right_amount_blocks*45 - 22
    offset_y = 77 + down_amount_blocks*45 - 22

    xcoord = left+offset_x
    ycoord = top+offset_y

    return xcoord, ycoord


def check_color(pixel_color, piece_color):
    treshold = 2
    for i in range(3):
        if pixel_color[i] not in range(piece_color[i]-treshold, piece_color[i]+treshold):
            return False
    return True



#def get_color_of_object(sideways, vertical):
def get_pixel_color(x_coordinate, y_coordinate):
    pixel_color = pyautogui.pixel(x_coordinate, y_coordinate)
    if(check_color(pixel_color, (26, 199, 242)) or check_color(pixel_color,(11, 125, 193))): # blue circle
        print_colored_text("¤",CYAN)
        return 1
    elif(check_color(pixel_color, (34, 102, 210)) or check_color(pixel_color,(14, 86, 181))): # blue square
        print_colored_text("¤",BLUE)
        return 2
    elif(check_color(pixel_color,(152, 216, 251)) or check_color(pixel_color,(62, 132, 197))): # blue octagon
        print_colored_text("¤",BRIGHT_WHITE)
        return 3
    elif(check_color(pixel_color,(76, 149, 140)) or check_color(pixel_color,(31, 105, 153))): # green octagon
        print_colored_text("¤",GREEN)
        return 4
    elif(check_color(pixel_color,(122, 219, 192)) or  check_color(pixel_color,(50, 133, 174))): # greencircle
        print_colored_text("¤",BRIGHT_GREEN)
        return 5
    elif(check_color(pixel_color,(21, 191, 199)) or  check_color(pixel_color,(9, 122, 177))): # greencircle
        print_colored_text("¤",BG_MAGENTA)
        return 6
    elif(check_color(pixel_color,(145, 132, 83)) or  check_color(pixel_color,(59, 98, 130))): # puffer Fish
        print_colored_text("¤",BRIGHT_YELLOW)
        return 69
    else:
        return -1

def get_pixel_color_rgb(x, y):
    pixel_color = pyautogui.pixel(x, y)
    print(pixel_color, end=" ")
    return 0

def get_all_pixel_colors(window):
    for y in range(12):
        for x in range(6):
            xcoord, ycoord = get_piece_coordinate(window, x+1, y+1)
            piece = get_pixel_color(xcoord, ycoord) # get_pixel_color_rgb Print For Values
            # _ = get_pixel_color_rgb(xcoord, ycoord) # get_pixel_color_rgb Print For Values
            gamestate[y][x] = piece
        # print("")

def ifpause():
    for y in range(12):
        for x in range(6):
            if gamestate[y][x] == -1:
                return True
    return False

def on_key_event(k):
    global STOP_FLAG
    if k.name == "esc":
        print("Stopping the script...")
        STOP_FLAG = True


if __name__ == "__main__":
    keyboard.hook(on_key_event)
    full_window_title = "Puzzle Pirates - Yolomaister on the Emerald ocean"  # Replace with your actual game window title

    print("Starting bot...")

    # Initialize gamestate array with 6x12 matrix of zeros
    gamestate = create_empty_array(6,12)

    # Get Game Window
    full_game_window = gw.getWindowsWithTitle(full_window_title)
    window = full_game_window[0]

    if window:
        window.activate() # Opens windows and uses.

        # get piece coordinates and store them in x, y variables
        x, y = get_piece_coordinate(window, 1, 1)

        # move mouse to coordinates with 0.5 second delay
        # left click
       # pyautogui.click()
        while not STOP_FLAG:
            get_all_pixel_colors(window)
            if ifpause():
                pyautogui.sleep(2)
                continue
            pufferxy = jotain.checkpuffer(gamestate)
            if pufferxy != (-1,-1):
                x, y = get_piece_coordinate(window, pufferxy[0]+1,pufferxy[1]+1)
                pyautogui.moveTo(x, y, duration=0.5)
                pyautogui.click()
                pyautogui.sleep(2)
                continue
            bestmove = jotain.getbestmove(gamestate, 2)
            print("Best move gives score:",bestmove[0])
            print("Swaps to make:")
            for i in range(1,len(bestmove)):
                print(f"{bestmove[i][0]+1} {bestmove[i][1]+1}")
                x, y = get_piece_coordinate(window, bestmove[i][0]+1, bestmove[i][1]+1)
                x += 10
                pyautogui.moveTo(x, y, duration=0.2)
                pyautogui.click()
                pyautogui.sleep(0.1)

            pyautogui.sleep(2)

    else:
        print(f"Game window with title '{full_window_title}' not found.")
