import os
import global_variables
import web_engine

from keyboard import add_hotkey
from obsidian_engine import *
from excel_engine import *
from console import show_console, hide_console
from obsidian_colleagues_and_alumni import update_colleagues_and_alumni_for_all_files, update_colleagues_and_alumni_for_single_file

def print_hotkeys():
    os.system('cls')
    print(f'{global_variables.app_title}\nList of Hotkeys\n{global_variables.app_separator}')

    for command in commands:
        if commands[command]['hotkey']:
            name = commands[command]['name']
            hotkey = commands[command]['hotkey']
            print(f'{name} - {hotkey}')

def print_commands():
    os.system('cls')
    print(f'{global_variables.app_title}\nList of Commands\n{global_variables.app_separator}')

    for command in commands:
        if commands[command]['commands']:
            name = commands[command]['name']
            command_list = str(commands[command]['commands'])
            print(f'{name} - {command_list}')

def parse_command():
    global_variables.active_input = True
    input_command = input('\n➡️ Enter a command: ')

    for command in commands:
        if input_command in commands[command]['commands']:
            commands[command]['function']()
            global_variables.active_input = False
            return True

    print('\n❌ Command not recognized. Please try again.')
    global_variables.active_input = False
    return False

commands = {
    #HOTKEYS & COMMANDS
    'l_s': {
        'commands': ['ls', 'list shortcuts', 'hotkeys', 'list hotkeys'],
        'name': 'Print Hotkeys',
        'hotkey': 'Alt+Q',
        'function': print_hotkeys
    },
    'l_c': {
        'commands': ['lc', 'list commands', 'commands'],
        'name': 'List Commands',
        'hotkey': 'Alt+A',
        'function': print_commands
    },
    'p_c': {
        'commands': ['pc', 'enter a command', 'command'],
        'name': 'Enter a Command',
        'hotkey': 'Alt+`',
        'function': parse_command
    },

    #CONSOLE
    's_c': {
        'commands': ['sc', 'show console'],
        'name': 'Show Console',
        'hotkey': 'Alt+S',
        'function': show_console
    },
    'h_c': {
        'commands': ['hc', 'hide console'],
        'name': 'Hide Console',
        'hotkey': 'Alt+H',
        'function': hide_console
    },

    #LINKS MANIPULATION
    'in_li_to_ob': {
        'commands': ['ilto', 'in li to ob', 'interesting link to obsidian'],
        'name': 'Interesting Link to Obsidian',
        'hotkey': 'Alt+I',
        'function': interesting_link_to_obsidian
    },

    # ADD ENTITY FROM LINKEDIN
    'add_n_tal_f_li': {
        'commands': ['antfl', 'add talent', 'at', 'add new talent from linkedin'],
        'name': 'Add New Talent from LinkedIn',
        'hotkey': 'Alt+T',
        'function': add_new_talent_from_linkedin
    },
    'add_n_con_f_li': {
        'commands': ['ancfl', 'add connection', 'ac', 'anc', 'add new connection', 'add new talent from linkedin'],
        'name': 'Add New Connection from LinkedIn',
        'hotkey': 'Alt+C',
        'function': add_new_connection_from_linkedin
    },
    'add_n_u_f_li': {
        'commands': ['anufl', 'add school', 'au', 'anu', 'add new school', 'add new school from linkedin', 'add college', 'add university'],
        'name': 'Add New School/University from LinkedIn',
        'hotkey': 'Alt+U',
        'function': add_new_school_from_linkedin
    },
    'add_n_m_f_li': {
        'commands': ['anmfl', 'add snooze', 'as', 'ans', 'add new snooze', 'add new snooze from linkedin messaging'],
        'name': 'Add New Snooze from LinkedIn Messaging',
        'hotkey': 'Alt+U',
        'function': add_new_school_from_linkedin
    },

    # OPEN ENTITIES IN OBSIDIAN
    'op_li_fl_ob': {
        'commands': ['olfo', 'op li fl ob', 'open linkedin file', 'open linkedin file in obsidian'],
        'name': 'Open LinkedIn File in Obsidian',
        'hotkey': 'Alt+O',
        'function': open_ideas_in_obsidian
    },
    'op_li_con_ob': {
        'commands': ['olco', 'op li con ob', 'open connection in obsidian'],
        'name': 'Open Connection in Obsidian',
        'hotkey': 'Ctrl+Alt+O',
        'function': open_connection_in_obsidian
    },
    'op_id_in_ob': {
        'commands': ['oiio', 'op id in ob', 'open ideas in obsidian', 'ideas', 'idea', 'ideapad', 'misli'],
        'name': 'Open Ideas in Obsidian',
        'hotkey': 'Alt+X',
        'function': open_ideas_in_obsidian
    },
    'op_il_in_ob': {
        'commands': ['oilo', 'op il in ob', 'open interesting links in obsidian', 'links', 'interesting links'],
        'name': 'Open Interesting Links in Obsidian',
        'hotkey': 'Ctrl+Alt+X',
        'function': open_interesting_links_in_obsidian
    },

    # EXCEL OPERATIONS
    'ch_if_com_ex_db': {
        'commands': ['ciyeid', 'ciyed', 'check if company exists in database'],
        'name': 'Check for Company in Database',
        'hotkey': 'Ctrl+Alt+W',
        'function': check_if_company_exists_in_database
    },
    'ch_if_cp_ex_db': {
        'commands': ['cicped'],
        'name': 'Check for Careers Page in Database',
        'hotkey': 'Ctrl+Alt+P',
        'function': check_if_careers_page_exists_in_database
    },
    'ap_com_to_db': {
        'commands': ['aytd'],
        'name': 'Append Company to Database',
        'hotkey': 'Alt+W',
        'function': append_company_to_database
    },
    'ap_cp_to_db': {
        'commands': ['acptd'],
        'name': 'Append Careers Page to Database',
        'hotkey': 'Alt+P',
        'function': append_careers_page_to_database
    },

    # EXCEL/WEB OPERATIONS
    'ch_for_v': {
        'commands': ['cfv', 'ch for v', 'check for vacancies', 'sfv', 'search for vacancies'],
        'name': 'Check for Vacancies from Database',
        'hotkey': '',
        'function': web_engine.search_for_vacancies
    },

    # COLLEAGUES AND ALUMNI OPERATIONS
    'up_cl_al_all': {
        'commands': ['ucaa', 'up cl al all', 'update colleagues and alumni for all files'],
        'name': 'Update Colleagues and Alumni for All Files',
        'hotkey': '',
        'function': update_colleagues_and_alumni_for_all_files
    },
    'up_cl_al_sf': {
        'commands': ['ucas', 'up cl al sf', 'update colleagues and alumni for current file'],
        'name': 'Update Colleagues and Alumni for current Files',
        'hotkey': '',
        'function': update_colleagues_and_alumni_for_single_file
    }
}
