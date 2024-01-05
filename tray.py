from PIL import Image
from pystray import MenuItem, Menu, Icon

import console

# Create the menu with quit and show options
def start_tray_menu():
    menu = Menu(
        MenuItem('Show', console.show_console),
        MenuItem('Hide', console.hide_console),
        MenuItem('', None),
        MenuItem('Quit', cleanup_and_quit)
    )

    # Create the system tray icon

    icon = Icon("Obsidian Tools", Image.open("./icon.ico"), menu=menu)
    icon.run()

# Function to handle the cleanup and quit the application
def cleanup_and_quit():
    exit()
