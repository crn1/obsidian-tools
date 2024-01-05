import os
import global_variables
import time
import bs4
from lxml import etree

def find_experience_section(tag):
    return tag.name == 'section' and 'Experience' in tag.get_text()

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

def scrape_linkedin_profile():
    html = global_variables.current_html
    soup = bs4.BeautifulSoup(html, 'html.parser')

    name = ''
    location = ''
    company = ''

    try:
        name = soup.select_one('h1')
        if name:
            print("Name: " + name.text.strip())
    except Exception as e:
        print(e)

    try:
        headline = soup.select_one('#profile-content > div > div > div > div > main > section > div > div > div:nth-child(1) > div.text-body-medium.break-words')
        if headline:
            print("Headline: " + headline.text.strip())
    except Exception as e:
        print(e)

    try:
        location = soup.select_one('#profile-content > div > div > div > div > main > section > div > div > div > span.text-body-small.inline.t-black--light.break-words')
        if location:
            print("Location: " + location.text.strip())
    except Exception as e:
        print(e)

    try:
        # Find the section containing the text "Experience"
        experience_section = soup.find(find_experience_section)

        # Check if the section is found
        if experience_section:
            # Now you can continue with your original CSS selector
            company = experience_section.select_one('div > ul > li:nth-child(1) > div > div > div > div > span:nth-child(2) > span:nth-child(1)')

            # Process the company data as needed
            if company:
                company = company.text.split(" · ", -1)[0]
                print("Company: " + company)
        else:
            print("Experience section not found.")

    except Exception as e:
            print(e)

def scrape_linkedin_company():
    html = global_variables.current_html
    soup = bs4.BeautifulSoup(html, 'html.parser')

    try:
        name = soup.select_one('h1')
        if name:
            print("Name: " + name.text.strip())
    except Exception as e:
        print(e)

    try:
        description = soup.select_one('* > div.relative > div.ph5.pb5 > div.org-top-card__primary-content.org-top-card-primary-content--zero-height-logo.org-top-card__improved-primary-content--ia > div.block.mt2 > div > p')
        if description:
            print("Description: " + description.text.strip())
    except Exception as e:
        print(e)

    try:
        industry = soup.select_one('* > div.relative > div.ph5.pb5 > div.org-top-card__primary-content.org-top-card-primary-content--zero-height-logo.org-top-card__improved-primary-content--ia > div.block.mt2 > div > div > div.org-top-card-summary-info-list__info-item')
        if industry:
            print("Indsutry: " + industry.text.strip())
    except Exception as e:
        print(e)

    try:
        location = soup.select_one('* > div.relative > div.ph5.pb5 > div.org-top-card__primary-content.org-top-card-primary-content--zero-height-logo.org-top-card__improved-primary-content--ia > div.block.mt2 > div > div > div.inline-block > div:nth-child(1)')
        if location:
            print("Location: " + location.text.strip())
    except Exception as e:
        print(e)

def add_new_talent_from_linkedin():
    current_url = global_variables.current_url
    current_html = global_variables.current_html
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
                scrape_linkedin_profile()
            elif global_variables.current_url.startswith("https://www.linkedin.com/company/"):
                search_for_entity(global_variables.obsidian_companies_path, "✅ ✅ ✅ IS IN CRM", "❌ ❌ ❌ NOT IN CRM")
                scrape_linkedin_company()
            else:
                print("Current URL: " + global_variables.current_url)
