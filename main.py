import sys
import signal
import pystray
from pystray import MenuItem as item, Menu as menu
from PIL import Image
import ctypes
import keyboard
from threading import Thread

from hotkeys import add_hotkeys
from chrome_engine import start_chrome_engine, shutdown_server

# Function to be executed when the quit option is selected
def quit_program(icon, item):
    icon.stop()
    sys.exit(0)

def hide_console():
    the_program_to_hide = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(the_program_to_hide, 0)  # SW_HIDE = 0

# Function to be executed when the show option is selected
def show_console():
    the_program_to_hide = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(the_program_to_hide, 9)  # SW_RESTORE = 9

# Function to handle the cleanup and quit the application
def cleanup_and_quit():
    icon.stop()
    sys.exit(0)

# Create the menu with quit and show options
menu = menu(
    item('Show', show_console),
    item('Hide', hide_console),
    item('', None),
    item('Quit', quit_program)
)

# Create the system tray icon
icon = pystray.Icon("name", Image.open("./icon.ico"), menu=menu)

# Add elementary hotkeys first, then add the rest
keyboard.add_hotkey("Alt+S", show_console)  # Show - Ctrl+S
keyboard.add_hotkey("Alt+H", hide_console) # Hide - Ctrl+H
keyboard.add_hotkey("Alt+0", cleanup_and_quit) # Hide - Ctrl+H

# Import all the hotkeys from hotkeys.py file
add_hotkeys()

# Run the console app
try:
    # Register the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, shutdown_server)

    # Create and start the HTTP server thread
    http_server_thread = Thread(target=start_chrome_engine)
    http_server_thread.start()

    # Create and start the PyStray thread
    pystray_thread = Thread(target=icon.run)
    pystray_thread.start()

    # Wait for both threads to finish
    http_server_thread.join()
    pystray_thread.join()

    icon.run()
    start_chrome_engine()
except KeyboardInterrupt:
    cleanup_and_quit(icon, None)
