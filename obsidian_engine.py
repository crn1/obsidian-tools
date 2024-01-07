import os
import global_variables
import time
import linkedin_scrapers
import re

def interesting_link_to_obsidian():
    # Specify the file path
    file_path = global_variables.obsidian_interesting_links_path
    current_url = global_variables.current_url

    global_variables.active_input = True

    url_name = input('Enter a name of the URL: ')

    try:
        with open(file_path, "a") as file:
            # Append the text, ensuring proper newline handling
            file.write(f"\n- [{url_name}]({current_url})")

        print("File successfully appended")

    except Exception as e:
        print(f"Error appending the file: {e}")

    global_variables.active_input = False

def add_new_contact_from_linkedin():
    name, headline, location, company_name = linkedin_scrapers.scrape_linkedin_profile()
    output_path = global_variables.obsidian_contacts_path
    template_file = global_variables.obsidian_contact_template_path
    add_new_entity_from_linkedin('in/', output_path, template_file, name=name, headline=headline, location=location, company_name=company_name)

def add_new_talent_from_linkedin():
    name, headline, location, company_name = linkedin_scrapers.scrape_linkedin_profile()
    output_path = global_variables.obsidian_talents_path
    template_file = global_variables.obsidian_talent_template_path
    add_new_entity_from_linkedin('in/', output_path, template_file, name=name, headline=headline, location=location, company_name=company_name)

def add_new_company_from_linkedin():
    name, description, location, industry = linkedin_scrapers.scrape_linkedin_company()
    output_path = global_variables.obsidian_companies_path
    template_file = global_variables.obsidian_company_template_path
    add_new_entity_from_linkedin('company/', output_path, template_file, name=name, description=description, location=location, industry=industry)

def add_new_entity_from_linkedin(linkedin_starts_with, output_path, template_file, name='', headline='', location='', company_name='', description='', industry=''):
    current_url = global_variables.current_url
    if not current_url.startswith(f'https://www.linkedin.com/{linkedin_starts_with}'):
        print("Error: You're not on valid LinkedIn URL for this action!")
        return False

    if search_for_entity(output_path):
        print("Error: The person is already in the system for this action!")
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
                new_file_content.append(f'Company: [[{output_path}{company_name}.md]]\n')
            elif "Headline: " in line and headline:
                new_file_content.append(f'Headline: {headline}\n')
            elif "Description: " in line and description:
                new_file_content.append(f'Headline: {description}\n')
            elif "Industry: " in line and industry:
                new_file_content.append(f'Headline: {industry}\n')
            else:
                new_file_content.append(line)

        output_file_path = os.path.join(output_path, f'{name}.md')
        with open(output_file_path, 'w') as file:
            file.writelines(new_file_content)

        print(f'File written to {output_file_path}')

    except Exception as e:
        print(e)

def search_for_entity(folder_path, message_found='', message_not_found='', print_message=True):
    try:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(global_variables.obsidian_talents_path, file_name)

            # Check if the path is a file and if it has the .md extension
            if os.path.isfile(file_path) and file_name.endswith(".md"):
                # Read the contents of the file and search for the URL
                with open(file_path, 'r') as file:
                    file_contents = file.read()

                    if global_variables.current_url in file_contents:
                        if print_message:
                            print(message_found)
                        return True

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
                search_for_entity(global_variables.obsidian_talents_path, "✅ ✅ ✅ ALREADY IN TALENT POOL", "❌ ❌ ❌ NOT IN TALENT POOL")
                print('\n')
                search_for_entity(global_variables.obsidian_contacts_path, "✅ ✅ ✅ IS CONTACT", "❌ ❌ ❌ NOT CONTACT")
            elif global_variables.current_url.startswith("https://www.linkedin.com/company/"):
                search_for_entity(global_variables.obsidian_companies_path, "✅ ✅ ✅ IS IN CRM", "❌ ❌ ❌ NOT IN CRM")
