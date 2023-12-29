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

gamestate: list[list[int]] = []


def print_colored_text(text, color_code):
    print(f"{color_code}{text}{RESET}", end=" ")


def create_empty_array(xsize: int, ysize: int) -> list[list[int]]:
    # Create a 2D array with zeros using lists
    return [[0 for _ in range(xsize)] for _ in range(ysize)]


def get_gameboard_top_left(window):
    left, top = window.left, window.top
    offset_x = 90 + 3
    offset_y = 77
    return left + offset_x, top + offset_y


def get_piece_coordinate(window, right_amount_blocks, down_amount_blocks):
    # Start From First Object
    left, top = window.left, window.top
    offset_x = 90 + 3 + right_amount_blocks * 45 - 22
    offset_y = 77 + down_amount_blocks * 45 - 22

    return left + offset_x, top + offset_y


def get_pixel_color(x_coordinate, y_coordinate):
    pixel_color = pyautogui.pixel(x_coordinate, y_coordinate)
    color_mapping = {
        (26, 199, 242): CYAN,
        (11, 125, 193): CYAN,
        (34, 102, 210): BLUE,
        (14, 86, 181): BLUE,
        (152, 216, 251): BRIGHT_WHITE,
        (62, 132, 197): BRIGHT_WHITE,
        (76, 149, 140): GREEN,
        (31, 105, 153): GREEN,
        (122, 219, 192): BRIGHT_GREEN,
        (50, 133, 174): BRIGHT_GREEN
    }

    for color, code in color_mapping.items():
        if pixel_color == color:
            print_colored_text("¤", code)
            return color_mapping[color]

    return RESET


def get_all_pixel_colors(window):
    for y in range(12):
        for x in range(6):
            xcoord, ycoord = get_piece_coordinate(window, x + 1, y + 1)
            piece = get_pixel_color(xcoord, ycoord)
        print()


def find_best_move():
    for y in range(12):
        for x in range(5):
            pass


def calculate_score(array):
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
    full_window_title = "Puzzle Pirates - Yolomaister on the Emerald ocean"  # Replace with your actual game window title

    print("Starting bot...")

    # Initialize gamestate array with 6x12 matrix of zeros
    gamestate = create_empty_array(6, 12)

    # Get Game Window
    full_game_window = gw.getWindowsWithTitle(full_window_title)
    window = full_game_window[0]
    window.activate()  # Opens windows and uses.

    if window:
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
