import os
import global_variables
import time
import linkedin_scrapers

def interesting_link_to_obsidian():
    # Specify the file path
    file_path = global_variables.obsidian_interesting_links_path
    current_url = global_variables.current_url

    global_variables.active_input = True

    url_name = input('Enter a name of the URL: ')

    try:
        with open(file_path, "a", encoding="utf-8") as file:
            # Append the text, ensuring proper newline handling
            file.write(f"\n- [{url_name}]({current_url})")

        print("File successfully appended")

    except Exception as e:
        print(f"Error appending the file: {e}")

    global_variables.active_input = False

def add_new_talent_from_linkedin():
    current_url = global_variables.current_url
    current_html = global_variables.current_html

    name, headline, location, company = linkedin_scrapers.scrape_linkedin_profile()
    print(f'name: {name}\nheadline: {headline}\nlocation:{location}\ncompany:{company}')
    return 0

def add_new_company_from_linkedin():
    current_url = global_variables.current_url
    current_html = global_variables.current_html

    name, description, location, industry = linkedin_scrapers.scrape_linkedin_company()
    print(f'name: {name}\ndescription: {description}\nlocation:{location}\nindustry:{industry}')
    return 0

def search_for_entity(folder_path, message_found, message_not_found, print_message=True):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(global_variables.obsidian_talents_path, file_name)

        # Check if the path is a file and if it has the .md extension
        if os.path.isfile(file_path) and file_name.endswith(".md"):
            # Read the contents of the file and search for the URL
            with open(file_path, 'r', encoding='utf-8') as file:
                file_contents = file.read()

                if url in file_contents:
                    if print_message:
                        print(message_found)
                    return file_path, file_name

    if print_message:
        print(message_not_found)
    return False

def obsidian_checker():
    while True:
        time.sleep(1)

        if not global_variables.active_input:

            os.system('cls')
            if global_variables.current_url.startswith("https://www.linkedin.com/in/"):
                search_for_entity(global_variables.obsidian_contacts_path, "✅ ✅ ✅ IS CONTACT", "❌ ❌ ❌ NOT CONTACT")
                search_for_entity(global_variables.obsidian_talents_path, "✅ ✅ ✅ ALREADY IN TALENT POOL", "❌ ❌ ❌ NOT IN TALENT POOL")
                add_new_talent_from_linkedin()
            elif global_variables.current_url.startswith("https://www.linkedin.com/company/"):
                search_for_entity(global_variables.obsidian_companies_path, "✅ ✅ ✅ IS IN CRM", "❌ ❌ ❌ NOT IN CRM")
                add_new_company_from_linkedin()
            else:
                print("Current URL: " + global_variables.current_url)
