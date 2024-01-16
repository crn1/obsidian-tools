import bs4
import global_variables

def is_experience_section(tag):
    return tag.name == 'section' and 'Experience' in tag.get_text() and 'Experienced' not in tag.get_text()
def is_education_section(tag):
    return tag.name == 'section' and 'Education' in tag.get_text()

def scrape_value(selector):
    html = global_variables.current_html
    value = ''
    try:
        soup = bs4.BeautifulSoup(html, 'html.parser')
        value = soup.select_one(selector).text.strip().replace('\n', '').replace('  ', ' ')
        # if value:
        #     print("Value: " + name.text.strip())
    except Exception as e:
        print(e)

    return value

def scrape_linkedin_messaging_name():
    return scrape_value('#thread-detail-jump-target')

def scrape_linkedin_profile_name():
    return scrape_value('h1')
def scrape_linkedin_profile_headline():
    return scrape_value('#profile-content > div > div > div > div > main > section > div > div > div:nth-child(1) > div.text-body-medium.break-words')
def scrape_linkedin_profile_location():
    return scrape_value('#profile-content > div > div > div > div > main > section > div > div > div > span.text-body-small.inline.t-black--light.break-words')

def scrape_linkedin_company_name():
    return scrape_value('h1')
def scrape_linkedin_company_description():
    return scrape_value('* > div.relative > div.ph5.pb5 > div.org-top-card__primary-content.org-top-card-primary-content--zero-height-logo.org-top-card__improved-primary-content--ia > div.block.mt2 > div > p')
def scrape_linkedin_company_location():
    return scrape_value('* > div.relative > div.ph5.pb5 > div.org-top-card__primary-content.org-top-card-primary-content--zero-height-logo.org-top-card__improved-primary-content--ia > div.block.mt2 > div > div > div.inline-block > div:nth-child(1)')
def scrape_linkedin_company_industry():
    return scrape_value('* > div.relative > div.ph5.pb5 > div.org-top-card__primary-content.org-top-card-primary-content--zero-height-logo.org-top-card__improved-primary-content--ia > div.block.mt2 > div > div > div.org-top-card-summary-info-list__info-item')

def scrape_linkedin_school_name():
    return scrape_value('h1')
def scrape_linkedin_school_description():
    return scrape_value('* > div.relative > div.ph5.pb5 > div.org-top-card__primary-content.org-top-card-primary-content--zero-height-logo.org-top-card__improved-primary-content--ia > div.block.mt2 > div > p')
def scrape_linkedin_school_location():
    return scrape_value('* > div.relative > div.ph5.pb5 > div.org-top-card__primary-content.org-top-card-primary-content--zero-height-logo.org-top-card__improved-primary-content--ia > div.block.mt2 > div > div > div.inline-block > div:nth-child(1)')

def get_target_section(section_name):
    target_section = None

    try:
        # Find the section containing the text "Experience"
        html = global_variables.current_html

        soup = bs4.BeautifulSoup(html, 'html.parser')
        sections = soup.select('#profile-content > div > div > div > div > main > section')

        # Search for target section
        for section in sections:
            if (section_name == "Experience" and is_experience_section(section)) or (section_name == "Education" and is_education_section(section)):
                target_section = section

    except Exception as e:
        print(e)

    return target_section


def scrape_linkedin_profile_companies():
    companies = []
    current_company_name = ''
    current_position = ''

    try:
        experience_section = get_target_section('Experience')

        # Check if the section is found
        if experience_section:
            # Select all experience items within the section
            experience_items = experience_section.select('div > ul > li > div > div > div > div')

            for index, item in enumerate(experience_items):
                current_company = {'Name': '', 'Position': '', 'StartDate': '', 'EndDate': ''}

                # Extract company and position from each item
                company_name = item.select_one('span:nth-child(2) > span:nth-child(1)')
                position = item.select_one('div > div > div > div > div > span:nth-child(1)')
                duration = item.select_one('span:nth-child(3) > span')

                # We don't need empty values!
                if not company_name or not duration:
                    continue

                if position:
                    current_company['Position'] = position.text.strip().replace('\n', '').replace('  ', ' ')

                current_company['Name'] = company_name.text.split(" · ")[0].strip().replace('\n', '').replace('  ', ' ')

                duration = duration.text.split(" · ")[0].strip()

                if duration:
                    current_company['StartDate'] = duration.split(" - ")[0].strip().replace('\n', '').replace('  ', ' ')

                    if len(duration.split(' - ')) > 1:
                        current_company['EndDate'] = duration.split(" - ")[1].strip().replace('\n', '').replace('  ', ' ')
                    else:
                        current_company['EndDate'] = current_company['StartDate']
                #if "Present" in duration_end:
                #    duration_end = ''

                companies.append(current_company)

                if index == 0:
                    if current_company['Name']:
                        current_company_name = current_company['Name']
                    if current_company['Position']:
                        current_position = current_company['Position']

        else:
            print("Experience section not found.")

    except Exception as e:
            print(e)

    if companies:
        return companies, current_company_name, current_position
    else:
        return '', current_company_name, current_position

def scrape_linkedin_profile_education():
    education = []
    current_school_name = ''
    current_degree = ''

    try:
        education_section = get_target_section('Education')

        # Check if the section is found
        if education_section:
            # Select all experience items within the section
            education_items = education_section.select('div > ul > li > div > div > div > a')

            for index, item in enumerate(education_items):
                current_education = {'Name': '', 'Degree': '', 'StartDate': '', 'EndDate': ''}

                # Extract school name, degree, and duration from each item
                school_name = item.select_one('div > div > div > div > span:nth-child(1)')
                degree = item.select_one('span:nth-child(2) > span:nth-child(1)')
                duration = item.select_one('span:nth-child(3) > span')

                # We don't need empty values!
                if not school_name or not duration:
                    continue

                if degree:
                    current_education['Degree'] = degree.text.strip().replace('\n', '').replace('  ', ' ')

                current_education['Name'] = school_name.text.split(" · ")[0].strip().replace('\n', '').replace('  ', ' ')

                current_education['StartDate'] = duration.text.split(" - ")[0].strip().replace('\n', '').replace('  ', ' ')
                if len(duration.text.split(' - ')) > 1:
                    current_education['EndDate'] = duration.text.split(" - ")[1].strip().replace('\n', '').replace('  ', ' ')
                else:
                    current_education['EndDate'] = current_education['StartDate']
                #if "Present" in duration_end:
                #    duration_end = ''

                education.append(current_education)

                if index == 0:
                    current_school_name = current_education['Name']

                    if current_education['Degree']:
                        current_degree = current_education['Degree']

        else:
            print("Education section not found.")

    except Exception as e:
            print(e)

    if education:
        return education, current_school_name, current_degree
    else:
        return '', current_school_name, current_degree
