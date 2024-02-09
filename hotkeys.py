import os
import commands_engine

from keyboard import add_hotkey
from obsidian_engine import *
from excel_engine import *
from console import show_console, hide_console
from obsidian_colleagues_and_alumni import update_colleagues_and_alumni_for_all_files, update_colleagues_and_alumni_for_single_file

def add_hotkeys():
    for command in commands_engine.commands:
        if commands_engine.commands[command]['hotkey']:
            add_hotkey(commands_engine.commands[command]['hotkey'], commands_engine.commands[command]['function'])
