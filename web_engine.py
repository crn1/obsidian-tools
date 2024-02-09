import requests

import global_variables
import companies_database
import web_common

from bs4 import BeautifulSoup
from excel_engine import get_rows

def search_for_vacancies():
    try:
        # Example usage:
        file_path = global_variables.obsidian_companies_database_path
        keywords = input('\n➡️ Enter keywords: ')
        tags_input = input("➡️ Enter tags (separate with space): ").strip().split()
        industry_input = input("➡️ Enter industry: ").strip()
        location_input = input("➡️ Enter location: ").strip()

        result = companies_database.search_careers_pages(file_path, tags=tags_input, industry=industry_input, location=location_input)
        print(result)

        #rows = get_rows(global_variables.obsidian_companies_database_path, 'Careers Pages')
        #for row in rows:
        #    current_url = row[0]
        #    if web_common.is_valid_url(current_url):
        #        if search_for_keyboard(current_url, keywords.split(' ')):
        #            print('Found keywords in {current_url}')

    except Exception as e:
        print(f'Error: {e}')

    return False

def search_for_keyword(url, keywords):
    html_content = web_common.get_html(url)
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract text content from the HTML
    text_content = soup.get_text()

    # Convert text content and keywords to lowercase for case-insensitive search
    text_content_lower = text_content.lower()
    keywords_lower = [keyword.lower() for keyword in keywords]

    # Perform boolean search
    results = {}
    for keyword in keywords_lower:
        if keyword in text_content_lower:
            return True

    return False
