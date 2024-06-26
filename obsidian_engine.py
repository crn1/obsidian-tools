import os
import global_variables
import time
import linkedin_scrapers
import webbrowser
import yaml
import web_common
import excel_engine

from dateutil.parser import parse

open_interesting_links_in_obsidian = lambda: open_file_in_obsidian(global_variables.obsidian_interesting_links_path)
open_ideas_in_obsidian = lambda: open_file_in_obsidian(global_variables.obsidian_ideas_path)
open_connection_in_obsidian = lambda: open_linkedin_file_in_obsidian(search_for_talent=False)

def write_file(output_path, name, new_file_content, update_file=False):
    """Writes content to a file, ensuring a unique filename if a file with the same name already exists.

    Args:
        output_path (str): The path to the output directory.
        name (str): The base name of the file (without extension).
        new_file_content (str): The content to write to the file.
    """
    base_filename = f'{name}.md' if not name.endswith('.md') else name
    file_path = os.path.join(output_path, base_filename)

    if not update_file:
        i = 1
        while os.path.exists(file_path):
            filename, extension = os.path.splitext(base_filename)
            unique_filename = f"{filename} - {i}{extension}"
            file_path = os.path.join(output_path, unique_filename)
            i += 1

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_file_content)

    print(f'File written to {file_path}\n')

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

def open_linkedin_file_in_obsidian(search_for_talent=True):
    current_url = global_variables.current_url

    if current_url.startswith('https://www.linkedin.com/company/'):
        folder_path = global_variables.obsidian_companies_path
    elif current_url.startswith('https://www.linkedin.com/school/'):
        folder_path = global_variables.obsidian_schools_path
    elif current_url.startswith('https://www.linkedin.com/messaging/thread/'):
        folder_path = global_variables.obsidian_snoozes_path
    elif current_url.startswith('https://www.linkedin.com/in/'):
        if search_for_talent:
            folder_path = global_variables.obsidian_talents_path
        else:
            folder_path = global_variables.obsidian_connections_path
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
        default_name = linkedin_scrapers.scrape_linkedin_messaging_name()
        name = input(f'URL Name (default is "{default_name}"): ') or default_name
    elif current_url.startswith(f'https://www.linkedin.com/in/'):
        default_name = linkedin_scrapers.scrape_linkedin_profile_name()
        name = input(f'URL Name (default is "{default_name}"): ') or default_name
    elif current_url.startswith(f'https://www.linkedin.com/company/'):
        default_name = linkedin_scrapers.scrape_linkedin_company_name()
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

    tags = input('Enter tags: ')
    description = input('Enter description: ')

    try:

        update_file = False
        if search_for_entity(output_path, current_url):
            print("The snooze is already in the system, updating the file instead.")
            template_file = search_for_entity(output_path, current_url)
            output_path, name = os.path.split(template_file)
            update_file = True

        with open(template_file, 'r', encoding='utf-8') as file:
            file_content = file.readlines()

        new_file_content = []
        for line in file_content:
            if "Link: " in line:
                new_file_content.append(f'Link: {current_url}\n')
            elif "Date: " in line:
                new_file_content.append(f'Date: {date}\n')
            elif "Tags: " in line:
                new_file_content.append(f'Tags: {tags}\n')
            elif "Description: " in line:
                new_file_content.append(f'Description: {description}\n')
            else:
                new_file_content.append(line)

        write_file(output_path, name, new_file_content, update_file)

    except Exception as e:
        print(e)
        return False

    global_variables.active_input = False

def add_new_connection_from_linkedin():
    name = linkedin_scrapers.scrape_linkedin_profile_name()
    headline = linkedin_scrapers.scrape_linkedin_profile_headline()
    location = linkedin_scrapers.scrape_linkedin_profile_location()
    companies, company, position = linkedin_scrapers.scrape_linkedin_profile_companies()
    education, university, degree = linkedin_scrapers.scrape_linkedin_profile_education()

    output_path = global_variables.obsidian_connections_path
    template_file = global_variables.obsidian_connection_template_path

    add_new_entity_from_linkedin('in/', output_path, template_file, name=name, headline=headline, location=location, companies=companies, company=company, position=position, education=education, university=university, degree=degree)

def add_new_talent_from_linkedin():
    name = linkedin_scrapers.scrape_linkedin_profile_name()
    headline = linkedin_scrapers.scrape_linkedin_profile_headline()
    location = linkedin_scrapers.scrape_linkedin_profile_location()
    companies, company, position = linkedin_scrapers.scrape_linkedin_profile_companies()
    education, university, degree = linkedin_scrapers.scrape_linkedin_profile_education()

    output_path = global_variables.obsidian_talents_path
    template_file = global_variables.obsidian_talent_template_path

    add_new_entity_from_linkedin('in/', output_path, template_file, name=name, headline=headline, location=location, companies=companies, company=company, position=position, education=education, university=university, degree=degree)

def add_new_company_from_linkedin():
    name = linkedin_scrapers.scrape_linkedin_company_name()
    description = linkedin_scrapers.scrape_linkedin_company_description()
    location = linkedin_scrapers.scrape_linkedin_company_location()
    industry = linkedin_scrapers.scrape_linkedin_company_industry()

    output_path = global_variables.obsidian_companies_path
    template_file = global_variables.obsidian_company_template_path

    add_new_entity_from_linkedin('company/', output_path, template_file, name=name, description=description, location=location, industry=industry)

def add_new_school_from_linkedin():
    name = linkedin_scrapers.scrape_linkedin_school_name()
    description = linkedin_scrapers.scrape_linkedin_school_description()
    location = linkedin_scrapers.scrape_linkedin_school_location()

    output_path = global_variables.obsidian_schools_path
    template_file = global_variables.obsidian_school_template_path

    add_new_entity_from_linkedin('school/', output_path, template_file, name=name, description=description, location=location)

def add_new_entity_from_linkedin(linkedin_starts_with, output_path, template_file, name='', headline='', location='', company='', companies='', description='', industry='', position='', education='', university='', degree=''):
    current_url = global_variables.current_url

    if not current_url.startswith(f'https://www.linkedin.com/{linkedin_starts_with}'):
        print("Error: You're not on valid LinkedIn URL for this action!")
        return False

    update_file = False

    try:
        # If the file is found, we're going to work with the found file and update it
        if search_for_entity(output_path, current_url):
            print("The entity is already in the system for this action, updating the file instead.")
            template_file = search_for_entity(output_path, current_url)
            output_path, name = os.path.split(template_file)
            update_file = True

        file_content = ''
        # We're opening the template_file which can either be the one passed from the arg or modified in the code above
        with open(template_file, "r", encoding='utf-8') as file:
            file_content = file.readlines()

        # Find the index of the SECOND "---\n" delimiter:
        frontmatter_end_index = file_content.index("---\n", file_content.index("---\n") + 1) + 1
        frontmatter_lines = file_content[:frontmatter_end_index]
        content_lines = file_content[frontmatter_end_index:]

        frontmatter_string = "".join(frontmatter_lines).replace('---\n', '')
        frontmatter_dict = yaml.safe_load(frontmatter_string)
        #print(frontmatter_dict)

        if web_common.company_url_specific_comparasion(current_url):
            frontmatter_dict['LinkedIn'] = web_common.normalize_company_url(current_url)
        else:
            frontmatter_dict['LinkedIn'] = current_url

        if location:
            frontmatter_dict['Location'] = location
        if company:
            frontmatter_dict['Company'] = company
        if companies:
            frontmatter_dict['Companies'] = companies
        if headline:
            frontmatter_dict['Headline'] = headline
        if description:
            frontmatter_dict['Description'] = description
        if industry:
            frontmatter_dict['Industry'] = industry
        if position:
            frontmatter_dict['Position'] = position
        if education:
            frontmatter_dict['Education'] = education
        if university:
            frontmatter_dict['University'] = university
        if degree:
            frontmatter_dict['Degree'] = degree

        updated_frontmatter_string = yaml.dump(frontmatter_dict, default_flow_style=False, allow_unicode=True).replace('null', '')
        #print(updated_frontmatter_string)
        updated_content = ['---\n'] + updated_frontmatter_string.splitlines(keepends=True) + ['---\n'] + content_lines

        write_file(output_path, name, updated_content, update_file=update_file)

    except Exception as e:
        print(e)

def search_for_entity(folder_path, check_variable, message_found='', message_not_found='', print_message=True):
    try:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            # Check if the path is a file and if it has the .md extension
            if os.path.isfile(file_path) and file_name.endswith(".md"):
                # Read the contents of the file and search for the URL
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_contents = file.read()

                    # SpecificCompany comparasion
                    if web_common.company_url_specific_comparasion(check_variable):
                        check_variable = web_common.normalize_company_url(check_variable)

                    if check_variable in file_contents:
                        if print_message:
                            print(message_found)
                        return file_path

        if print_message:
            print(message_not_found)

    except Exception as e:
        print(e)

    return False

check_if_company_exists_in_obsidian = lambda: search_for_entity(
    global_variables.obsidian_companies_path,
    global_variables.current_url,
    "✅ IS IN CRM\n",
    "❌ NOT IN CRM\n")

check_if_talent_exists_in_obsidian = lambda: search_for_entity(
    global_variables.obsidian_talents_path,
    global_variables.current_url,
    "✅ IS IN TALENT POOL",
    "❌ NOT IN TALENT POOL")

check_if_connection_exists_in_obsidian = lambda: search_for_entity(
    global_variables.obsidian_connections_path,
    global_variables.current_url,
    "✅ IS IN CRM\n",
    "❌ NOT IN CRM\n")

check_if_snooze_exists_in_obsidian = lambda: search_for_entity(
    global_variables.obsidian_snoozes_path,
    global_variables.current_url,
    "✅ IS IN SNOOZE",
    "❌ NOT IN SNOOZE")

def obsidian_checker():
    while True:
        current_url = global_variables.current_url
        time.sleep(0.5)

        if current_url != global_variables.current_url and not global_variables.active_input:
            os.system('cls||clear')
            # print(f'🌐 URL: {global_variables.current_url}\n')

            if global_variables.current_url.startswith("https://www.linkedin.com/in/"):
                check_if_talent_exists_in_obsidian()
                print('')
                check_if_connection_exists_in_obsidian()
            elif global_variables.current_url.startswith("https://www.linkedin.com/company/"):
                check_if_company_exists_in_obsidian()
                excel_engine.check_if_linkedin_company_exists_in_database()
            else:
                excel_engine.check_if_careers_page_exists_in_database()

            if not global_variables.current_url.startswith('https://www.linkedin.com/'):
                excel_engine.check_if_company_exists_in_database()

            # Search for snooze anyway, always
            check_if_snooze_exists_in_obsidian()
