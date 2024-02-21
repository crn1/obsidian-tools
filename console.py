import ctypes
import os
import global_variables

# Function to manipulate the window based on the provided code
manipulate_window = lambda codes: [ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), code) for code in codes]

# Lambda functions for specific window manipulations
hide_console = lambda: manipulate_window([0])  # SW_HIDE = 0
show_console = lambda: manipulate_window([0, 9])  # SW_HIDE = 0, SW_RESTORE = 9
maximize_console = lambda: manipulate_window([0, 9, 3])  # SW_HIDE = 0, SW_SHOWMAXIMIZED = 3
minimize_console = lambda: manipulate_window([0, 9, 2])  # SW_HIDE = 0, SW_SHOWMINIMIZED = 2

def clear_console():
    os.system('cls')
    print(global_variables.app_title)
    print('Alt + Q to list all hotkeys')
    print('Alt + A to list all commands')
    print('Alt + ` to enter a command')
    print(global_variables.app_separator)
