import os
import json
import global_variables

def get_current_note_path():
    try:
        obsidian_config_path = os.path.join(global_variables.obsidian_vault_path, '.obsidian', 'workspace.json')

        with open(obsidian_config_path, 'r', encoding='utf-8') as config_file:
            config_data = json.load(config_file)
            tab_index = config_data.get('main').get('children')[0].get('currentTab', 0)
            active_note_filename = config_data.get('main').get('children')[0].get('children')[tab_index].get('state').get('state').get('file', '')

            if active_note_filename:
                return active_note_filename.replace('\\', '/')
            else:
                return False

    except Exception as e:
        print(e)

    return False
