import global_variables
import web_common
import pandas as pd
import asyncio
import os
import playwright

from bs4 import BeautifulSoup
from excel_engine import get_rows
from playwright.async_api import async_playwright

async def download_rendered_html(context, url, keywords):
    page = await context.new_page()
    try:
        await page.goto(url, timeout=5000)
        await page.wait_for_load_state("networkidle")

        html = await page.content()
        await search_for_keyword(html, url, keywords)

    except Exception as e:
        print(f"\nError for {url}: {e}")

    finally:
        await page.close()

async def async_websites_download(urls, keywords):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()

        semaphore = asyncio.Semaphore(10)
        tasks = []

        for url in urls:
            task = asyncio.create_task(download_rendered_html(context, url, keywords))
            tasks.append(task)

        await asyncio.gather(*tasks)
        await browser.close()

    print('Websites are finished scraping.')

async def search_for_keyword(html, url, keywords):
    try:
        print(f"Searching for {url}")

        if not isinstance(html, str):
            html = str(html)

        # make the html lower-case for case insensitivity
        html = html.lower()

        for keyword in keywords:
            if keyword.lower() not in html:
                return False

        print(f'✅ Found {keyword} in {url}')
        return True

    except Exception as e:
        print(f"Error: {e}")

    return False

def search_for_vacancies():
    print('\n* * * Check for Vacancies * * *')
    try:
        # Example usage:
        # Assuming companies_database is properly imported
        file_path = global_variables.obsidian_companies_database_path
        keywords = input('\n➡️ Enter keywords (separate by comma ,): ').strip().split(', ') or []
        tags_input = input("➡️ Enter tags (separate by comma ,): ").strip().split(', ') or []
        industry_input = input("➡️ Enter industry (separate by comma ,): ").strip().split(', ') or []
        location_input = input("➡️ Enter location (separate by comma ,): ").strip().split(', ') or []
        department_input = input("➡️ Enter department (separate by comma ,): ").strip().split(', ') or []
        office_input = input("➡️ Enter office (separate by comma ,): ").strip().split(', ') or []

        os.system('cls')
        print(f'Filtering companies . . .')
        result = search_careers_pages(file_path, tags=tags_input, industry=industry_input, location=location_input, department=department_input, office=office_input)

        print(result)

        # print(f'Searching for websites . . .')
        # asyncio.run(async_websites_download(result, keywords))

    except Exception as e:
        print(f'Error: {e}')

    return False

def load_excel_data(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        companies_df = pd.read_excel(xls, 'Companies (ALL)')
        careers_df = pd.read_excel(xls, 'Careers Pages')
        return companies_df, careers_df

    except Exception as e:
        print("An error occurred while loading the Excel file: ", e)
        return None, None

def filter_companies(companies_df, tags=None, industry=None, location=None, department=None, office=None):
    try:
        filtered_df = companies_df.copy()

        # Tags: exact match for any item in the list
        if tags and tags != ['']:
            filtered_df = filtered_df[filtered_df['Tags'].apply(lambda x: any(tag in x.split(', ') for tag in tags))]
            #filtered_df = filtered_df[filtered_df['Tags'].apply(lambda x: all(tag in x.split(', ') for tag in tags))]

        # Others: substring match using str.contains (case-insensitive)
        if industry:
            for industry_term in industry:
                if industry_term:
                    filtered_df = filtered_df[filtered_df['Industry'].str.contains(industry_term, case=False, na=False)]
        if location:
            for location_term in location:
                if location_term:
                    filtered_df = filtered_df[filtered_df['Location'].str.contains(location_term, case=False, na=False)]
        if department:
            for department_term in department:
                if department_term:
                    filtered_df = filtered_df[filtered_df['Department'].str.contains(department_term, case=False, na=False)]
        if office:
            for office_term in office:
                if office_term:
                    filtered_df = filtered_df[filtered_df['Office'].str.contains(office_term, case=False, na=False)]

        return filtered_df

    except Exception as e:
        print("An error occurred while filtering companies:", e)
        return pd.DataFrame()

def match_careers_pages(filtered_careers, filtered_companies=None):
    try:
        if filtered_companies is not None:
            matched_df = pd.merge(filtered_companies, filtered_careers, on='Website URL', how='inner')
        else:
            matched_df = filtered_careers.copy()

        return matched_df['Careers URL'].tolist()

    except Exception as e:
        print("An error occurred while matching companies with careers pages:", e)
        return []

def search_careers_pages(file_path, tags=None, industry=None, location=None, department=None, office=None):
    try:
        companies_df, careers_df = load_excel_data(file_path)

        if careers_df is None or companies_df is None:
            return []

        filtered_companies = filter_companies(companies_df, tags, industry, location)
        filtered_careers = filter_companies(careers_df, department=department, office=office)

        # Check if there are any filtered companies left after filtering
        if filtered_companies.empty:
            return []

        # Check if there are any filtered careers pages left after filtering
        if filtered_careers.empty:
            return []

        urls = match_careers_pages(filtered_careers, filtered_companies)

        return urls

    except Exception as e:
        print("An unexpected error occurred: ", e)
        return []
