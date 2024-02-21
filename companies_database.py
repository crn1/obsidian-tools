import global_variables
import web_common
import pandas as pd
import asyncio
import os
import playwright
import console
import time
import uuid
import datetime

from excel_engine import get_rows
from playwright.async_api import async_playwright, expect

async def scroll_down_while_possible(page, url, calm_down=True, sleep_time=1.5):
    try:
        await page.evaluate(
            """
            var intervalID = setInterval(function () {
                var scrollingElement = (document.scrollingElement || document.body);
                scrollingElement.scrollTop = scrollingElement.scrollHeight;
            }, 200);

            """
        )

        prev_height = None
        while True:
            curr_height = await page.evaluate('(window.innerHeight + window.scrollY)')
            if not prev_height:
                prev_height = curr_height

                # Sleep anyway for one second, just in case
                time.sleep(sleep_time)
                if calm_down:
                    await page_calm_down(page, url)

            elif prev_height == curr_height:
                await page.evaluate('clearInterval(intervalID)')
                break

            else:
                prev_height = curr_height
                time.sleep(sleep_time)

                if calm_down:
                    await page_calm_down(page, url)

    except Exception as e:
        print(f"❌ Error scrolling on {url}: {e}")

async def load_page(page, url, timeout=10000, calm_down=True, xpath=None):
    # Loading the URL provided
    if web_common.is_valid_xpath(xpath):
        print(f'Loading page on {url} with xpath {xpath}')
    else:
        pass
        print(f'Loading page on {url}')

    try:
        await page.goto(url, timeout=timeout)

        if calm_down:
            await page_calm_down(page, url)

    except Exception as e:
        print(f"❌ Error for {url}: {e}")
        return False

async def element_click(page, element, url, calm_down=True):
    try:
        await element.click(force=True)

        if calm_down:
            await page_calm_down(page, url)

    except Exception as e:
        print(f"❌ Error for the element {str(element)}: {e}")
        return False

async def page_calm_down(page, url, timeout=10000):
    #print(f'Waiting for networkidle on {url}')
    try:
        # Wait for networkidle or other stability signals
        await page.wait_for_load_state("networkidle", timeout=timeout)
        return True

    except Exception as e:
        print(f"❌ Error for {url}: {e}")
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

async def download_rendered_html(context, url, xpath, keywords, result_path, link_hop=0, click_count=0, current_html=None):

    max_link_hops = 3
    max_clicks = 10

    page = await context.new_page()
    # Loading the URL provided
    await load_page(page, url, xpath=xpath)

    try:
        while click_count < max_clicks and link_hop < max_link_hops and web_common.is_valid_xpath(xpath):

            #Scroll down until the end of the page to load dynamic content just in case
            await scroll_down_while_possible(page, url)

            # Find the targeted element using xpath
            element = page.locator(xpath)
            if element:
                #print(f'click_count={click_count}\nlink_hop={link_hop}')

                # Click on the found element, it's wait automatically for networkidle
                await element_click(page, element, url)

                new_url = page.url
                #print(f'URL: {url}\nNew URL: {new_url}')

                if url != new_url:
                    link_hop += 1

                    # Scenario 1: Dynamic URL and content loading, RECRUSIVE
                    #print(f'Element {str(element)} on {url} changes current URL (Scenario 2)')
                    await download_rendered_html(
                        context, href, xpath, keywords, result_path, link_hop, click_count, new_html
                    )

                    # Finally break the while loop
                    break

                else:
                    click_count += 1

                    # Scenario 2: Dynamic content loading
                    #print(f'Element {str(element)} on {url} does not change the current URL')
                    #print('Loading content . . .')
                    new_html = await page.content()
                    if new_html == current_html:
                        #print(f'No HTML/content changes for {str(element)} on {url}, breaking . . .')
                        break  # No changes, stop waiting
                    else:
                        #print(f'Clicking on {str(element)} changes the URL, iterating . . .')
                        current_html = new_html

            # If element doesn't exist or isn't clickable, break
            else:
                print(f'XPath {xpath} not valid or found on {url}')
                print(f'Trying with a standard playwright load . . .')
                break

        await process_final_html(page, url, keywords, result_path)

    except Exception as e:
        print(f"❌ Error for {url}: {e}")

    finally:
        pass
        await page.close()

async def async_websites_download(urls, xpaths, keywords, result_path):

    print('Searching websites . . .')

    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        driver_dir = os.path.join(dir_path, 'chromedriver')
        #cookies_extension_dir = os.path.join(dir_path, 'cookies_extension')

        # On Windows at least, cookies_extension needs to be copied to ms-playwirght installation path!
        cookies_extension_dir = 'cookies_extension'
        #log_directory = os.path.join(driver_dir, 'awesome.log')
        #print(f'Running Chromium Driver from driver_dir: {driver_dir}')
        #print(f'Loading Cookies Extension from cookies_extension_dir: {cookies_extension_dir}')

        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                driver_dir,
                headless=False,
                args=[
                    #'--enable-logging',
                    #'--log-level=DEBUG',
                    #f'--log-file={log_directory}',
                    f'--disable-extensions-except={cookies_extension_dir}',
                    f'--load-extension={cookies_extension_dir}'
                ]
            )

            semaphore = asyncio.Semaphore(10)
            tasks = []

            for url, xpath in zip(urls, xpaths):
                task = asyncio.create_task(download_rendered_html(context, url, xpath, keywords, result_path))
                tasks.append(task)

            await asyncio.gather(*tasks)
            await context.close()

        print('✅ Websites are finished scraping.')

    except Exception as e:
        print(f"❌ Error while running async_websites_download: {e}")

async def search_for_keyword(html, url, keywords, result_path):
    try:
        print(f'Searching keywords for {url}')

        if not isinstance(html, str):
            html = str(html)

        # make the html and keywords string lower-case for case insensitivity
        html = html.lower()
        keywords = keywords.lower()

        # Split the keywords by 'or'
        or_keywords = keywords.split(' or ')

        # Iterate over 'or' groups
        for or_keyword in or_keywords:
            and_keywords = or_keyword.split()

            # Initialize flag for 'and' condition
            all_and_keywords_found = True

            # Iterate over 'and' conditions within each 'or' group
            for and_keyword in and_keywords:
                if and_keyword not in html:
                    all_and_keywords_found = False
                    break

            # If all 'and' conditions are satisfied, return True
            if all_and_keywords_found:
                print(f'✅ Found {or_keyword} in {url}')

                #Append the result to a file
                append_results_file(result_path, url)

                return True

        # If none of the 'or' groups matched
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
            print(f'{result} successfully written to the results file.')

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
            file.write(f'\nSearch results for "{str(keywords)}"')
            file.write(f'\nDate: {current_date}')
            file.write(f'\nTags: {str(tags)}')
            file.write(f'\nIndsutry: {str(industry)}')
            file.write(f'\nLocation: {str(location)}')
            file.write(f'\nDepartment: {str(department)}')
            file.write(f'\nOffice: {str(office)}')
            file.write(f'\n{global_variables.app_separator}')

        print(f'Result file result-{unique_name}-{date_for_file_name}.txt has been created')
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
            keywords = str(input('\n➡️ Enter keywords (separate by space and OR operator): ')).strip()
            if not keywords:
                print("❌ Keywords can't be empty, please try again!")
            else:
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

        os.system('cls')
        print(f'Filtering companies . . .')
        urls, xpaths = search_careers_pages(file_path, tags=tags_input, industry=industry_input, location=location_input, department=department_input, office=office_input)

        if urls:
            result_path = prepare_results_file(keywords, tags_input, industry_input, location_input, department_input, office_input)
            asyncio.run(async_websites_download(urls, xpaths, keywords, result_path))

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
        xpaths = matched_df['Next Button Xpath'].tolist()

        return urls, xpaths

    except Exception as e:
        print("An error occurred while matching companies with careers pages:", e)
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
        print("An error occurred while searching for careers pages: ", e)
        return [], []
