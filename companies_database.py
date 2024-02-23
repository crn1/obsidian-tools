import global_variables
import web_common
import pandas as pd
import asyncio
import os
import playwright
import console
import uuid
import datetime
import time

from excel_engine import get_rows
from playwright.async_api import async_playwright, expect

async def scroll_down_while_possible(page, url):
    try:
        await page.wait_for_timeout(1500)
        prev_height = await page.evaluate('document.body.scrollHeight')

        while True:
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)');
            await page.wait_for_timeout(1500)

            curr_height = await page.evaluate('document.body.scrollHeight')

            if prev_height == curr_height:
                break
            else:
                prev_height = curr_height

    except Exception as e:
        print(f"❌ Error scrolling on {url}: {e}")

async def load_page(page, url, calm_down=True, xpath=None):
    # Loading the URL provided
    if web_common.is_valid_xpath(xpath):
        print(f'📄 Loading page on {url} with xpath {xpath}')
    else:
        pass
        print(f'📄 Loading page on {url}')

    try:
        await page.goto(url)

    except Exception as e:
        print(f"❌ Error for {url}: {e}")
        return False

    if calm_down:
        await page_calm_down(page, url)

async def page_calm_down(page, url):
    try:
        # Wait for networkidle or other stability signals
        await page.wait_for_load_state("networkidle")
        return True

    except Exception as e:
        print(f"⚠️ Error while waiting for networkidle on {url}: {e}")
        return False

async def process_final_html(page, url, keywords, result_path, calm_down=True):
    if calm_down:
        await page_calm_down(page, url)

    try:
        # Get final rendered HTML
        #print(f'Waiting page content on {url}')
        html = await page.content()

        # Finally search for the keywords
        await search_for_keyword(html, url, keywords, result_path)

    except Exception as e:
        print(f"❌ Error for {url}: {e}")

async def download_rendered_html(context, url, xpath, keywords, result_path):

    page = await context.new_page()
    # Loading the URL provided
    await load_page(page, url, xpath=xpath)

    max_clicks = 20
    click_count = 0
    current_html = await page.content()
    await page_calm_down(page, url)
    await scroll_down_while_possible(page, url)

    try:
        while click_count < max_clicks and web_common.is_valid_xpath(xpath):

            # Find the targeted element using xpath
            element = page.locator(xpath)
            if element:

                await element.click()

                click_count += 1

                await scroll_down_while_possible(page, url)

                new_html = await page.content()
                if new_html == current_html:
                    #print(f'No HTML/content changes for {str(element)} on {url}, breaking . . .')
                    break  # No changes, stop waiting
                else:
                    #print(f'Clicking on {str(element)} changes the URL, iterating . . .')
                    current_html = new_html

            # If element doesn't exist or isn't clickable, break
            else:
                print(f'❌ XPath {xpath} not valid or found on {url}')
                break


        await process_final_html(page, url, keywords, result_path)

    except Exception as e:
        print(f"❌ Error for {url}: {e}")

    finally:
        await page.close()

async def async_websites_download(urls, xpaths, keywords, result_path):

    print('Searching websites . . .')
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        driver_dir = os.path.join(dir_path, 'chromedriver')

        # On Windows at least, cookies_extension needs to be copied to ms-playwirght installation path!
        cookies_extension_dir = 'cookies_extension'

        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                driver_dir,
                headless=False,
                args=[
                    f'--disable-extensions-except={cookies_extension_dir}',
                    f'--load-extension={cookies_extension_dir}'
                ]
            )

            semaphore = asyncio.Semaphore(30)  # Semaphore to limit concurrency

            async def download_with_semaphore(url, xpath):
                async with semaphore:
                    await download_rendered_html(context, url, xpath, keywords, result_path)

            # Create tasks with semaphore limit
            tasks = [download_with_semaphore(url, xpath) for url, xpath in zip(urls, xpaths)]

            await asyncio.gather(*tasks)
            await context.close()

        print('✅ Websites are finished scraping.')

    except Exception as e:
        print(f"❌ Error while running async_websites_download: {e}")

async def search_for_keyword(html, url, keywords, result_path):
    try:
        print(f'🔎 Searching keywords for {url}')

        if not isinstance(html, str):
            html = str(html)

        # make the html and keywords string lower-case for case insensitivity
        html = html.lower()

        # Iterate over 'or' groups
        for keyword in keywords:
            if keyword.lower() in html:
                print(f'✅ Found {keyword} in {url}')

                #Append the result to a file
                append_results_file(result_path, url)

                return True

        # print(f'❌ Keywords not found in {url}')
        return False

    except Exception as e:
        print(f"❌ Error: {e}")

        # Return False in case of any exception
        return False

def append_results_file(file_name, result):
    try:
        with open(file_name, 'a') as file:
            file.write(f'\n{result}')
            print(f'📝 {result} successfully written to the results file.')

    except Exception as e:
        print(f"❌ Error while appending to a results file: {e}")
        return False

def prepare_results_file(keywords, tags, industry, location, department, office):
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        results_dir = os.path.join(dir_path, 'search_results')

        # Create the folder if it doesn't exist
        if not os.path.exists(results_dir):
            os.makedirs(results_dir )

        # Generate a unique identifier
        unique_name = str(uuid.uuid4().hex)[:8]  # Using the first 8 characters of a UUID hex representation

        # Define the file name with a unique identifier
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        date_for_file_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')

        file_name = os.path.join(results_dir, f'result-{unique_name}-{date_for_file_name}.txt')

        # Write the list to the file
        with open(file_name, 'w') as file:
            file.write(f'{global_variables.app_title}')
            file.write(f'\nSearch results for {str(keywords)}')
            file.write(f'\nDate: {current_date}')
            file.write(f'\nTags: {str(tags)}')
            file.write(f'\nIndsutry: {str(industry)}')
            file.write(f'\nLocation: {str(location)}')
            file.write(f'\nDepartment: {str(department)}')
            file.write(f'\nOffice: {str(office)}')
            file.write(f'\n{global_variables.app_separator}')

        print(f'📝 Result file result-{unique_name}-{date_for_file_name}.txt has been created')
        return file_name

    except Exception as e:
        print(f"❌ Error while preparing the results file: {e}")
        return False

def search_for_vacancies():
    print('\n* * * Check for Vacancies * * *')

    urls = []
    xpaths = []
    try:
        # Example usage:
        # Assuming companies_database is properly imported
        file_path = global_variables.obsidian_companies_database_path

        while True:
            keywords_input = str(input("➡️ Enter keywords (separate by comma ,): ")).strip()
            if not keywords_input:
                print("❌ Keywords can't be empty, please try again!")
            else:
                keywords_input = keywords_input.split(', ')
                break

        tags_input = str(input("➡️ Enter tags (separate by comma ,): ")).strip()
        tags_input = tags_input.split(', ') if tags_input else []

        industry_input = str(input("➡️ Enter industry (separate by comma ,): ")).strip()
        industry_input = industry_input.split(', ') if industry_input else []

        location_input = str(input("➡️ Enter location (separate by comma ,): ")).strip()
        location_input = location_input.split(', ') if location_input else []

        department_input = str(input("➡️ Enter department (separate by comma ,): ")).strip()
        department_input = department_input.split(', ') if department_input else []

        office_input = str(input("➡️ Enter office (separate by comma ,): ")).strip()
        office_input = office_input.split(', ') if office_input else []

        os.system('cls||clear')
        print(f'Filtering companies . . .')
        urls, xpaths = search_careers_pages(file_path, tags=tags_input, industry=industry_input, location=location_input, department=department_input, office=office_input)

        if urls:
            result_path = prepare_results_file(keywords_input, tags_input, industry_input, location_input, department_input, office_input)
            asyncio.run(async_websites_download(urls, xpaths, keywords_input, result_path))

    except Exception as e:
        print(f'❌ Error: {e}')

    return False

def load_excel_data(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        companies_df = pd.read_excel(xls, 'Companies (ALL)')
        careers_df = pd.read_excel(xls, 'Careers Pages')
        return companies_df, careers_df

    except Exception as e:
        print("❌ An error occurred while loading the Excel file: ", e)
        return None, None

def filter_companies(companies_df, tags=None, industry=None, location=None, department=None, office=None):
    try:
        filtered_df = companies_df.copy()

        # Tags: exact match for any item in the list
        if tags:
            filtered_df = filtered_df[filtered_df['Tags'].apply(lambda x: any(tag in str(x).split(', ') for tag in tags))]
            #filtered_df = filtered_df[filtered_df['Tags'].apply(lambda x: all(tag in str(x).split(', ') for tag in tags))]

        # Others: substring match using str.contains (case-insensitive)
        if industry:
            industry_filters = [filtered_df['Industry'].str.contains(str(industry_term), case=False, na=False) for industry_term in industry if industry_term]
            if industry_filters:
                filtered_df = filtered_df[pd.concat(industry_filters, axis=1).any(axis=1)]
        if location:
            location_filters = [filtered_df['Location'].str.contains(str(location_term), case=False, na=False) for location_term in location if location_term]
            if location_filters:
                filtered_df = filtered_df[pd.concat(location_filters, axis=1).any(axis=1)]
        if department:
            department_filters = [filtered_df['Department'].str.contains(str(department_term), case=False, na=False) for department_term in department if department_term]
            if department_filters:
                filtered_df = filtered_df[pd.concat(department_filters, axis=1).any(axis=1)]
        if office:
            office_filters = [filtered_df['Office'].str.contains(str(office_term), case=False, na=False) for office_term in office if office_term]
            if office_filters:
                filtered_df = filtered_df[pd.concat(office_filters, axis=1).any(axis=1)]

        return filtered_df

    except Exception as e:
        print("❌ An error occurred while filtering companies:", e)
        return pd.DataFrame()

def match_careers_pages(filtered_careers, filtered_companies=None):
    try:
        if filtered_companies is not None:
            matched_df = pd.merge(filtered_companies, filtered_careers, on='Website URL', how='inner')
        else:
            matched_df = filtered_careers.copy()

        urls = matched_df['Careers URL'].tolist()
        xpaths = matched_df['Load More Xpath'].tolist()

        return urls, xpaths

    except Exception as e:
        print('❌ An error occurred while matching companies with careers pages:', e)
        return [], []

def search_careers_pages(file_path, tags=None, industry=None, location=None, department=None, office=None):
    try:
        companies_df, careers_df = load_excel_data(file_path)

        if careers_df is None or companies_df is None:
            return [], []

        filtered_companies = filter_companies(companies_df, tags=tags, industry=industry, location=location)
        filtered_careers = filter_companies(careers_df, department=department, office=office)

        # Check if there are any filtered companies left after filtering
        if filtered_companies.empty or filtered_careers.empty:
            print(f'⚠️ There are no filtered companies nor careers pages for this search!')
            return [], []

        urls, xpaths = match_careers_pages(filtered_careers, filtered_companies)

        return urls, xpaths

    except Exception as e:
        print('❌ An error occurred while searching for careers pages: ', e)
        return [], []
