import os

from keyboard import add_hotkey
from obsidian_engine import *
from console import show_console, hide_console
from obsidian_colleagues_and_alumni import update_colleagues_and_alumni_for_all_files, update_colleagues_and_alumni_for_single_file

HOTKEY_SHOW_CONSOLE = 'Alt+S'
HOTKEY_HIDE_CONSOLE = 'Alt+H'

HOTKEY_INTERESTING_LINK_TO_OBSIDIAN = 'Alt+I'

HOTKEY_ADD_NEW_TALENT_FROM_LINKEDIN = 'Alt+T'
HOTKEY_ADD_NEW_CONNECTION_FROM_LINKEDIN = 'Alt+C'
HOTKEY_ADD_NEW_COMPANY_FROM_LINKEDIN = 'Alt+Y'
HOTKEY_ADD_NEW_SCHOOL_FROM_LINKEDIN = 'Alt+U'
HOTKEY_ADD_NEW_SNOOZE_FROM_LINKEDIN_MESSAGING = 'Alt+M'

HOTKEY_OPEN_LINKEDIN_FILE_IN_OBSIDIAN = 'Alt+O'
HOTKEY_OPEN_CONNECTION_IN_OBSIDIAN = 'Ctrl+Alt+O'

HOTKEY_OPEN_INTERESTING_LINKS_IN_OBSIDIAN = 'Ctrl+Alt+X'
HOTKEY_OPEN_IDEAS_IN_OBSIDIAN = 'Alt+X'

HOTKEY_UPDATE_COLLEAGUES_AND_ALUMNI_FOR_ALL_FILES = 'Ctrl+Alt+.'
HOTKEY_UPDATE_COLLEAGUES_AND_ALUMNI_FOR_SINGLE_FILE = 'Alt+.'

HOTKEY_PRINT_HELP = 'Alt+Q'

def add_hotkeys():
    add_hotkey(HOTKEY_PRINT_HELP, print_help)

    add_hotkey(HOTKEY_SHOW_CONSOLE, show_console)
    add_hotkey(HOTKEY_HIDE_CONSOLE, hide_console)

    add_hotkey(HOTKEY_INTERESTING_LINK_TO_OBSIDIAN, interesting_link_to_obsidian)

    add_hotkey(HOTKEY_ADD_NEW_TALENT_FROM_LINKEDIN, add_new_talent_from_linkedin)
    add_hotkey(HOTKEY_ADD_NEW_CONNECTION_FROM_LINKEDIN, add_new_connection_from_linkedin)
    add_hotkey(HOTKEY_ADD_NEW_COMPANY_FROM_LINKEDIN, add_new_company_from_linkedin)
    add_hotkey(HOTKEY_ADD_NEW_SCHOOL_FROM_LINKEDIN, add_new_school_from_linkedin)
    add_hotkey(HOTKEY_ADD_NEW_SNOOZE_FROM_LINKEDIN_MESSAGING, add_new_snooze_from_linkedin_messaging)

    add_hotkey(HOTKEY_OPEN_LINKEDIN_FILE_IN_OBSIDIAN, open_linkedin_file_in_obsidian)
    add_hotkey(HOTKEY_OPEN_CONNECTION_IN_OBSIDIAN, open_connection_in_obsidian)

    add_hotkey(HOTKEY_OPEN_INTERESTING_LINKS_IN_OBSIDIAN, open_interesting_links_in_obsidian)
    add_hotkey(HOTKEY_OPEN_IDEAS_IN_OBSIDIAN, open_ideas_in_obsidian)

    add_hotkey(HOTKEY_UPDATE_COLLEAGUES_AND_ALUMNI_FOR_ALL_FILES, update_colleagues_and_alumni_for_all_files)
    add_hotkey(HOTKEY_UPDATE_COLLEAGUES_AND_ALUMNI_FOR_SINGLE_FILE, update_colleagues_and_alumni_for_single_file)

def print_help():
    os.system('cls')

    help_string = f"""Hotkeys List\n-----------------------------
List of all Shortcuts = {HOTKEY_PRINT_HELP}
Hide Console = {HOTKEY_SHOW_CONSOLE}
Show Console = {HOTKEY_HIDE_CONSOLE}
Interesting Link to Obsidian = {HOTKEY_INTERESTING_LINK_TO_OBSIDIAN}
Add New Talent from LinkedIn =  {HOTKEY_ADD_NEW_TALENT_FROM_LINKEDIN}
Add New Connection from LinkedIn = {HOTKEY_ADD_NEW_CONNECTION_FROM_LINKEDIN}
Add New Company from LinkedIn = {HOTKEY_ADD_NEW_COMPANY_FROM_LINKEDIN}
Add New School from LinkedIn =  {HOTKEY_ADD_NEW_SCHOOL_FROM_LINKEDIN}
Add New Snooze from LinkedIn Messaging = {HOTKEY_ADD_NEW_SNOOZE_FROM_LINKEDIN_MESSAGING}
Open Connection in Obsidian = {HOTKEY_OPEN_CONNECTION_IN_OBSIDIAN}
Open LinkedIn File in Obsidian = {HOTKEY_OPEN_LINKEDIN_FILE_IN_OBSIDIAN}
Open Interesting Links in Obsidian = {HOTKEY_OPEN_CONNECTION_IN_OBSIDIAN}
Open Ideas in Obsidian = {HOTKEY_OPEN_IDEAS_IN_OBSIDIAN}
Update Colleagues (All Files) = {HOTKEY_UPDATE_COLLEAGUES_AND_ALUMNI_FOR_ALL_FILES}
Update Colleagues (Single File) = {HOTKEY_UPDATE_COLLEAGUES_AND_ALUMNI_FOR_SINGLE_FILE}"""

    print(help_string)
