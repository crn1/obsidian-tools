import ctypes
import os
import global_variables

def hide_console():
    the_program_to_hide = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(the_program_to_hide, 0)  # SW_HIDE = 0

# Function to be executed when the show option is selected
def show_console():
    the_program_to_hide = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(the_program_to_hide, 0)  # SW_HIDE = 0
    ctypes.windll.user32.ShowWindow(the_program_to_hide, 9)  # SW_RESTORE = 9

def clear_console():
    os.system('cls')
    print(global_variables.app_title)
    print('Alt + Q to list all hotkeys')
    print('Alt + A to list all commands')
    print('Alt + ` to enter a command')
    print(global_variables.app_separator)
