import pygetwindow as gw
import pyautogui
import time

RESET = '\033[0m'
BLUE = '\033[34m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_CYAN = '\033[96m'
GREEN = '\033[32m'
CYAN = '\033[36m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_WHITE = '\033[97m'


gamestate : list[list[int]] = []

def print_colored_text(text, color_code):
    print(f"{color_code}{text}{RESET}", end=" ")

def create_empty_array(xsize: int, ysize: int) -> list[list[int]]:

    # Create a 2D array with zeros using lists
    two_d_array = [[0 for _ in range(ysize)] for _ in range(xsize)]

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

#def get_color_of_object(sideways, vertical):
def get_pixel_color(x_coordinate, y_coordinate):
    pixel_color = pyautogui.pixel(x_coordinate, y_coordinate)
    if(pixel_color == (26, 199, 242) or  pixel_color == (11, 125, 193)): # blue circle
        print_colored_text("¤",CYAN)
        return 1
    elif(pixel_color == (34, 102, 210) or  pixel_color == (14, 86, 181)): # blue square
        print_colored_text("¤",BLUE)
        return 2
    elif(pixel_color == (152, 216, 251) or pixel_color == (62, 132, 197)): # blue octagon
        print_colored_text("¤",BRIGHT_WHITE)
        return 3
    elif(pixel_color == (76, 149, 140) or pixel_color == (31, 105, 153)): # green octagon
        print_colored_text("¤",GREEN)
        return 4
    elif(pixel_color == (122, 219, 192) or  pixel_color == (50, 133, 174)): # greencircle
        print_colored_text("¤",BRIGHT_GREEN)
        return 5

def get_all_pixel_colors(window):
    for y in range(12):
        for x in range(6):
            xcoord, ycoord = get_piece_coordinate(window, x+1, y+1)
            piece = get_pixel_color(xcoord, ycoord)
            gamestate[y][x] = piece
        print("")

def explode():



def find_best_move():
    for y in range(12):
        for x in range(5):
            pass



def calculate_score(array:):
    def calculate_group_score(lst):
        score = 0
        count = 1
        for i in range(1, len(lst)):
            if lst[i] == lst[i - 1]:
                count += 1
            else:
                if count >= 3:
                    score += count
                count = 1
        if count >= 3:
            score += count
        return score

    def transpose(matrix):
        return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

    total_score = 0

    # Calculate score for rows
    for row in array:
        total_score += calculate_group_score(row)

    # Calculate score for columns
    for column in transpose(array):
        total_score += calculate_group_score(column)

    return total_score


if __name__ == "__main__":
    full_window_title = "Puzzle Pirates - Urbanman on the Emerald ocean"  # Replace with your actual game window title

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
        pyautogui.moveTo(x, y, duration=0.5)

        # left click
        pyautogui.click()
        time.sleep(1)


        # if object_found:
        #     # Interact with the object (e.g., click on it)
        #     pyautogui.click(100, 200)
        get_all_pixel_colors(window)
        print("Bot finished.")
    else:
        print(f"Game window with title '{full_window_title}' not found.")
