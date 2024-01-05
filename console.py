import ctypes
import os

def hide_console():
    the_program_to_hide = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(the_program_to_hide, 0)  # SW_HIDE = 0

# Function to be executed when the show option is selected
def show_console():
    the_program_to_hide = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(the_program_to_hide, 9)  # SW_RESTORE = 9

def clear_console():
    os.system('cls')
    print('* * * Obsidian Tools v1 by crn1 * * *')
