import os
import global_variables
import time
import linkedin_scrapers
import re
from dateutil.parser import parse
import webbrowser

open_interesting_links_in_obsidian = lambda: open_file_in_obsidian(global_variables.obsidian_interesting_links_path)
open_ideas_in_obsidian = lambda: open_file_in_obsidian(global_variables.obsidian_ideas_path)

def write_file(output_path, name, new_file_content):
    """Writes content to a file, ensuring a unique filename if a file with the same name already exists.

    Args:
        output_path (str): The path to the output directory.
        name (str): The base name of the file (without extension).
        new_file_content (str): The content to write to the file.
    """

    base_filename = f"{name}.md"
    file_path = os.path.join(output_path, base_filename)

    i = 1
    while os.path.exists(file_path):
        filename, extension = os.path.splitext(base_filename)
        unique_filename = f"{filename} - {i}{extension}"
        file_path = os.path.join(output_path, unique_filename)
        i += 1

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_file_content)

    print(f'File written to {file_path}')

def open_file_in_obsidian(file_path):
    try:
        vault_name = global_variables.obsidian_vault_name

        # Remove abs path and leave only what is needed for file arg in Obsidian's URI
        file_path = file_path.replace(global_variables.obsidian_vault_path, '')
        file_path = file_path.replace('\\', '/')

        uri = f"obsidian://open?vault={vault_name}&file={file_path}"
        webbrowser.open(uri)
    except Exception as e:
        print('\n' + e)

open_contact_in_obsidian = lambda: open_linkedin_file_in_obsidian(search_for_talent=False)

def open_linkedin_file_in_obsidian(search_for_talent=True):
    current_url = global_variables.current_url

    if current_url.startswith('https://www.linkedin.com/company'):
        folder_path = global_variables.obsidian_companies_path
    elif current_url.startswith('https://www.linkedin.com/messaging/thread/'):
        folder_path = global_variables.obsidian_snoozes_path
    elif current_url.startswith('https://www.linkedin.com/in/'):
        if search_for_talent:
            folder_path = global_variables.obsidian_talents_path
        else:
            folder_path = global_variables.obsidian_contacts_path
    else:
        print('Error: The link is not supported for opening!')
        return False

    file_path = search_for_entity(folder_path, current_url, print_message=False)

    if not file_path:
        print('Error: The file does not exist in the system')
        return False

    open_file_in_obsidian(file_path)

def interesting_link_to_obsidian():
    # Specify the file path
    file_path = global_variables.obsidian_interesting_links_path
    current_url = global_variables.current_url

    global_variables.active_input = True

    url_name = input('Enter a name of the URL: ')

    try:
        with open(file_path, "a", encoding='utf-8') as file:
            # Append the text, ensuring proper newline handling
            file.write(f"\n- [{url_name}]({current_url})")

        print("File successfully appended")

    except Exception as e:
        print(f"Error appending the file: {e}")

    global_variables.active_input = False

def add_new_snooze_from_linkedin_messaging():
    output_path = global_variables.obsidian_snoozes_path
    template_file = global_variables.obsidian_snooze_template_path
    current_url = global_variables.current_url

    global_variables.active_input = True

    if current_url.startswith(f'https://www.linkedin.com/messaging/thread/'):
        default_name = linkedin_scrapers.scrape_linkedin_messaging()
        name = input(f'URL Name (default is "{default_name}"): ') or default_name
    elif current_url.startswith(f'https://www.linkedin.com/in/'):
        default_name, a, b, c, d = linkedin_scrapers.scrape_linkedin_profile()
        name = input(f'URL Name (default is "{default_name}"): ') or default_name
    elif current_url.startswith(f'https://www.linkedin.com/company/'):
        default_name, a, b, c = linkedin_scrapers.scrape_linkedin_company()
        name = input(f'URL Name (default is "{default_name}"): ') or default_name
    else:
        name = input('URL Name: ')

    while True:
        try:
            date = input('Enter the date: ')
            date = parse(date, fuzzy=True)
            break
        except Exception as e:
            print(e)

    tag = input('Enter tags: ')
    description = input('Enter description: ')

    try:
        with open(template_file, "r") as file:
            file_content = file.readlines()

        new_file_content = []
        for line in file_content:
            if "Link: " in line:
                new_file_content.append(f'Link: {current_url}\n')
            elif "Date: " in line:
                new_file_content.append(f'Date: {date}\n')
            elif "Tag: " in line:
                new_file_content.append(f'Tag: {tag}\n')
            elif "Description: " in line:
                new_file_content.append(f'Description: {description}\n')
            else:
                new_file_content.append(line)

        write_file(output_path, name, new_file_content)

    except Exception as e:
        print(e)
        return False

    global_variables.active_input = False

def add_new_contact_from_linkedin():
    name, headline, location, company_name, position = linkedin_scrapers.scrape_linkedin_profile()
    output_path = global_variables.obsidian_contacts_path
    template_file = global_variables.obsidian_contact_template_path
    add_new_entity_from_linkedin('in/', output_path, template_file, name=name, headline=headline, location=location, company_name=company_name, position=position)

def add_new_talent_from_linkedin():
    name, headline, location, company_name, position = linkedin_scrapers.scrape_linkedin_profile()
    output_path = global_variables.obsidian_talents_path
    template_file = global_variables.obsidian_talent_template_path
    add_new_entity_from_linkedin('in/', output_path, template_file, name=name, headline=headline, location=location, company_name=company_name, position=position)

def add_new_company_from_linkedin():
    name, description, location, industry = linkedin_scrapers.scrape_linkedin_company()
    output_path = global_variables.obsidian_companies_path
    template_file = global_variables.obsidian_company_template_path
    add_new_entity_from_linkedin('company/', output_path, template_file, name=name, description=description, location=location, industry=industry)

def add_new_entity_from_linkedin(linkedin_starts_with, output_path, template_file, name='', headline='', location='', company_name='', description='', industry='', position=''):
    current_url = global_variables.current_url
    if not current_url.startswith(f'https://www.linkedin.com/{linkedin_starts_with}'):
        print("Error: You're not on valid LinkedIn URL for this action!")
        return False

    if search_for_entity(output_path, current_url):
        print("Error: The entity is already in the system for this action!")
        return False

    try:
        with open(template_file, "r") as file:
            file_content = file.readlines()

        new_file_content = []
        for line in file_content:
            if "LinkedIn: " in line:
                new_file_content.append(f'LinkedIn: {current_url}\n')
            elif "Location: " in line and location:
                new_file_content.append(f'Location: {location}\n')
            elif "Company: " in line and company_name:
                new_file_content.append(f'Company: {company_name}\n')
            elif "Headline: " in line and headline:
                new_file_content.append(f'Headline: {headline}\n')
            elif "Description: " in line and description:
                new_file_content.append(f'Description: {description}\n')
            elif "Industry: " in line and industry:
                new_file_content.append(f'Industry: {industry}\n')
            elif "Position: " in line and position:
                new_file_content.append(f'Position: {position}\n')
            else:
                new_file_content.append(line)

        write_file(output_path, name, new_file_content)

    except Exception as e:
        print(e)

def search_for_entity(folder_path, check_variable, message_found='', message_not_found='', print_message=True):
    try:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            # Check if the path is a file and if it has the .md extension
            if os.path.isfile(file_path) and file_name.endswith(".md"):
                # Read the contents of the file and search for the URL
                with open(file_path, 'r') as file:
                    file_contents = file.read()

                    if check_variable in file_contents:
                        if print_message:
                            print(message_found)
                        return file_path

        if print_message:
            print(message_not_found)

    except Exception as e:
        print(e)

    return False

def obsidian_checker():
    while True:
        time.sleep(1)

        if not global_variables.active_input:

            os.system('cls')
            print(f'Current URL: {global_variables.current_url}\n')

            if global_variables.current_url.startswith("https://www.linkedin.com/in/"):
                search_for_entity(global_variables.obsidian_talents_path, global_variables.current_url, "✅ ✅ ✅ ALREADY IN TALENT POOL", "❌ ❌ ❌ NOT IN TALENT POOL")
                print('')
                search_for_entity(global_variables.obsidian_contacts_path, global_variables.current_url, "✅ ✅ ✅ IS CONTACT", "❌ ❌ ❌ NOT CONTACT")
            elif global_variables.current_url.startswith("https://www.linkedin.com/company/"):
                search_for_entity(global_variables.obsidian_companies_path, global_variables.current_url, "✅ ✅ ✅ IS IN CRM", "❌ ❌ ❌ NOT IN CRM")
            elif global_variables.current_url.startswith("https://www.linkedin.com/messaging/thread/"):
                search_for_entity(global_variables.obsidian_snoozes_path, global_variables.current_url, "✅ ✅ ✅ IS IN SNOOZE", "❌ ❌ ❌ NOT IN SNOOZE")
