import os
import yaml
import re
import global_variables
import obsidian_common
from dateutil.parser import parse
from datetime import datetime

def update_the_file_with_new_matched_arrays(matched_colleagues, matched_alumni, current_file):
    try:
        current_file.seek(0)  # Rewind to the beginning of the file
        lines = current_file.readlines()

        if lines:
            write_index = 0

            for i, line in enumerate(lines):
                #print(line)
                if '# Colleagues' in line:  # Found the marker line
                    write_index = i  # Stop writing at this index
                    break

            if write_index == 0:
                for i, line in enumerate(lines):
                    if '# Alumni' in line:  # Found the marker line
                        write_index = i  # Stop writing at this index
                        break

            # Write index should always be the last row because if it stays 0, the wole file is going to be deleted
            if write_index == 0:
                write_index = len(lines)

            #print(f'{matched_alumni} and {matched_colleagues} to {current_file.name} from the line {write_index}\n')
            current_file.seek(0)  # Rewind to the beginning of the file
            current_file.truncate()  # Delete existing content
            current_file.writelines(lines[:write_index])  # Write original lines up to the marker

            # Append new colleagues section
            if matched_colleagues:
                current_file.write("### Colleagues\n")
                for colleague in matched_colleagues:
                    current_file.write(colleague)

            # Append new alumni section
            if matched_alumni:
                if matched_colleagues:
                    current_file.write("\n\n### Alumni\n")
                else:
                    current_file.write("### Alumni\n")
                for alum in matched_alumni:
                    current_file.write(alum)
        else:
            print('No lines found, aborting operation in order not to jeopardize data')

    except Exception as e:
        print(e)

def normalize_duration(duration):
    try:
        if duration.isdigit() and len(duration) <= 4:
            return parse(f"1st of January {duration}", fuzzy=True)

        if duration == "Present" or duration == "present":
            return datetime.now()

        parsed_duration = parse(duration, fuzzy=True)
        parsed_duration = parsed_duration.replace(day=1)
        return parsed_duration

    except Exception as e:
        print(e)

def is_common_duration(current_duration_start, comparasion_duration_start, current_duration_end=None, comparasion_duration_end=None):
    try:
        if current_duration_start and comparasion_duration_start:

            current_duration_start = normalize_duration(current_duration_start)
            comparasion_duration_start = normalize_duration(comparasion_duration_start)

            if current_duration_end and comparasion_duration_end:
                current_duration_end = normalize_duration(current_duration_end)
                comparasion_duration_end = normalize_duration(comparasion_duration_end)

                if current_duration_start <= comparasion_duration_end and current_duration_end >= comparasion_duration_start:
                    return True

            else:
                if current_duration_start.year == comparasion_duration_start.year:
                    return True

    except Exception as e:
        print(e)

    return False

def compare_durations(current_organizations, comparasion_organizations, person_path, organization_file_path, comparasion_filename, entity_name=''):
    result = []

    person_path = person_path.replace(global_variables.obsidian_vault_path, '')
    person_path = person_path.replace('\\', '/')

    organization_file_path = organization_file_path.replace(global_variables.obsidian_vault_path, '')
    organization_file_path = organization_file_path.replace('\\', '/')

    if current_organizations and comparasion_organizations:
        try:
            for current_organization in current_organizations:
                for comparasion_organization in comparasion_organizations:

                    if current_organization['Name'] == comparasion_organization['Name'] and \
                        current_organization['Name'] not in global_variables.forbidden_company_names:

                        current_duration_start = current_organization['StartDate']
                        comparasion_duration_start = comparasion_organization['StartDate']

                        current_duration_end = None if entity_name == 'Alum' else current_organization['EndDate']
                        comparasion_duration_end = None if entity_name == 'Alum' else comparasion_organization['EndDate']

                        if is_common_duration(current_duration_start, comparasion_duration_start, current_duration_end, comparasion_duration_end):

                            current_organization_name = current_organization['Name']
                            comparasion_organization_name = current_organization['Name']
                            comparasion_file_path = os.path.join(person_path, comparasion_filename).replace('\\', '/')

                            if entity_name == "Alum":
                                matched_string = f'\n- {entity_name}: [[{comparasion_file_path}]] at [[{organization_file_path}{current_organization_name}]] in {current_duration_start}'
                            else:
                                max_duration_start = current_duration_start if normalize_duration(current_duration_start) >= normalize_duration(comparasion_duration_start) else comparasion_duration_start
                                min_duration_end = current_duration_end if normalize_duration(current_duration_end) <= normalize_duration(comparasion_duration_end) else comparasion_duration_end
                                matched_string = f'\n- {entity_name}: [[{comparasion_file_path}]] at [[{organization_file_path}{current_organization_name}]] from {max_duration_start} to {min_duration_end}'

                            result.append(matched_string)

        except Exception as e:
            print(e)

    return result

def get_frontmatter_property(content, property_name, is_list=False):
    frontmatter_property = [] if is_list else ''

    try:
        frontmatter_match = re.search(r"^---\n(.*?)\n---", content, flags=re.DOTALL)
        if frontmatter_match:
            frontmatter_str = frontmatter_match.group(1)
            frontmatter = yaml.safe_load(frontmatter_str)

            # Extract the list property
            frontmatter_property = frontmatter.get(property_name)  # Replace with the actual property name

        else:
            print("No YAML frontmatter found in the file.")

    except Exception as e:
        print(e)

    return frontmatter_property

# This function will be called from hotkeys.py
def update_colleagues_and_alumni_for_all_files():
    compare_all_files_with_all_others(global_variables.obsidian_connections_path)
    compare_all_files_with_all_others(global_variables.obsidian_talents_path)

def update_colleagues_and_alumni_for_single_file():
    compare_single_file_with_all_others()

def compare_single_file_with_all_others():
    global_variables.active_input = True
    print('Started updating colleagues and alumni . . .')

    try:
        current_note_path = obsidian_common.get_current_note_path()
        if current_note_path:
            person_path, current_filename = os.path.split(os.path.join(global_variables.obsidian_vault_path, current_note_path))
            compare_current_file_with_all_others(person_path, current_filename)
            print(f'Finished updating {current_note_path}')

        else:
            print('current_note returned false or an empty string!')

    except Exception as e:
        print(e)

    global_variables.active_input = False

def compare_all_files_with_all_others(person_path):
    global_variables.active_input = True
    os.system('cls||clear')
    print('Started updating colleagues and alumni . . .')

    try:
        # List all files and then compare them all in compare_current_file_with_all_others() function
        for current_file_index, current_filename in enumerate(os.listdir(person_path)):
            if current_filename.endswith(".md"):  # Optional: filter by file extension
                compare_current_file_with_all_others(person_path, current_filename)

            # Print something in case the vault becomes too large
            if current_file_index % 50 == 0:
                print(f'Info: current_file_index is now at {current_file_index} . . .')

    except Exception as e:
        print(e)

    print('Finished updating colleagues and alumni.')
    global_variables.active_input = False

def compare_current_file_with_all_others(person_path, current_filename):
    companies_path = global_variables.obsidian_companies_path
    schools_path = global_variables.obsidian_schools_path
    current_file_path = os.path.join(person_path, current_filename)

    current_companies = []
    current_education = []
    matched_colleagues = []
    matched_alumni = []

    # Work with current file, r+ becuase we're going to use the same current_file in update_the_file_with_new_matched_arrays function
    with open(current_file_path, 'r+', encoding='utf-8') as current_file:

        # current_file_content is a string of the file contents that's going to be used to get YAML frontmatter property in active Obsidian file
        current_file_content = current_file.read()
        current_companies = get_frontmatter_property(current_file_content, 'Companies', is_list=True)
        current_education = get_frontmatter_property(current_file_content, 'Education', is_list=True)

        # List all the files for finding comparasion file
        for comparasion_file_index, comparasion_filename in enumerate(os.listdir(person_path)):
            if comparasion_filename.endswith(".md") and current_filename != comparasion_filename:  # Optional: filter by file extension
                comparasion_file_path = os.path.join(person_path, comparasion_filename)

                # Work with comparasion file
                with open(comparasion_file_path, 'r', encoding='utf-8') as current_comparasion_file:
                    current_comparasion_file_content = current_comparasion_file.read()
                    comparasion_companies = get_frontmatter_property(current_comparasion_file_content, 'Companies', is_list=True)
                    comparasion_education = get_frontmatter_property(current_comparasion_file_content, 'Education', is_list=True)

                    matched_colleagues.extend(compare_durations(current_companies, comparasion_companies, person_path, companies_path, comparasion_filename, entity_name='Colleague'))
                    matched_alumni.extend(compare_durations(current_education, comparasion_education, person_path, schools_path, comparasion_filename, entity_name='Alum'))

        # Finally, update everything, note the indentation! We update everything AFTER matched_colleagues and alumni got populated
        update_the_file_with_new_matched_arrays(matched_colleagues, matched_alumni, current_file)
