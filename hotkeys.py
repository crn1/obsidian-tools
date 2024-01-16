import keyboard
import obsidian_engine
import obsidian_colleagues_and_alumni
import console

def add_hotkeys():

    keyboard.add_hotkey("Alt+S", console.show_console)  # Show - Ctrl+S
    keyboard.add_hotkey("Alt+H", console.hide_console) # Hide - Ctrl+H

    keyboard.add_hotkey("Alt+I", obsidian_engine.interesting_link_to_obsidian)

    keyboard.add_hotkey("Alt+T", obsidian_engine.add_new_talent_from_linkedin)
    keyboard.add_hotkey("Alt+C", obsidian_engine.add_new_contact_from_linkedin)
    keyboard.add_hotkey("Alt+Y", obsidian_engine.add_new_company_from_linkedin)
    keyboard.add_hotkey("Alt+U", obsidian_engine.add_new_school_from_linkedin)
    keyboard.add_hotkey("Alt+M", obsidian_engine.add_new_snooze_from_linkedin_messaging)

    keyboard.add_hotkey("Alt+O", obsidian_engine.open_linkedin_file_in_obsidian)
    keyboard.add_hotkey("Ctrl+Alt+O", obsidian_engine.open_contact_in_obsidian)

    keyboard.add_hotkey("Ctrl+Alt+X", obsidian_engine.open_interesting_links_in_obsidian)
    keyboard.add_hotkey("Alt+X", obsidian_engine.open_ideas_in_obsidian)

    keyboard.add_hotkey("Alt+.", obsidian_colleagues_and_alumni.update_all_colleagues_and_alumni)
