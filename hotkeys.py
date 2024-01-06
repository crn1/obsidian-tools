import keyboard
import obsidian_engine
import console

def add_hotkeys():
    keyboard.add_hotkey("Alt+S", console.show_console)  # Show - Ctrl+S
    keyboard.add_hotkey("Alt+H", console.hide_console) # Hide - Ctrl+H
    keyboard.add_hotkey("Alt+I", obsidian_engine.interesting_link_to_obsidian)
    keyboard.add_hotkey("Alt+T", obsidian_engine.add_new_talent_from_linkedin)

