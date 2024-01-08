import bs4
import global_variables
import unicodedata

def find_experience_section(tag):
    return tag.name == 'section' and 'Experience' in tag.get_text() and 'Experienced' not in tag.get_text()

def scrape_linkedin_messaging():
    html = global_variables.current_html

    name = ''

    try:
        soup = bs4.BeautifulSoup(html, 'html.parser')
    except Exception as e:
        print(e)
        return name

    try:
        name = soup.select_one('#thread-detail-jump-target').text.strip()
        if name:
            print("Name: " + name)
    except Exception as e:
        print(e)

    return name


def scrape_linkedin_profile():
    html = global_variables.current_html

    name = ''
    headline = ''
    location = ''
    company = ''

    try:
        soup = bs4.BeautifulSoup(html, 'html.parser')
    except Exception as e:
        print(e)
        return name, headline, location, company

    try:
        name = soup.select_one('h1').text.strip()
        # if name:
        #     print("Name: " + name.text.strip())
    except Exception as e:
        print(e)

    try:
        headline = soup.select_one('#profile-content > div > div > div > div > main > section > div > div > div:nth-child(1) > div.text-body-medium.break-words').text.strip()
        # if headline:
        #     print("Headline: " + headline.text.strip())
    except Exception as e:
        print(e)

    try:
        location = soup.select_one('#profile-content > div > div > div > div > main > section > div > div > div > span.text-body-small.inline.t-black--light.break-words').text.strip()
        # if location:
        #     print("Location: " + location.text.strip())
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
                company = company.text.split(" · ")[0].strip()
                # print("Company: " + company)
        else:
            print("Experience section not found.")

    except Exception as e:
            print(e)

    return name, headline, location, company

def scrape_linkedin_company():
    html = global_variables.current_html

    name = ''
    description = ''
    location = ''
    industry = ''

    try:
        soup = bs4.BeautifulSoup(html, 'html.parser')
    except Exception as e:
        print(e)
        return name, description, location, industry

    try:
        name = soup.select_one('h1').text.strip()
        # if name:
        #     print("Name: " + name.text.strip())
    except Exception as e:
        print(e)

    try:
        description = soup.select_one('* > div.relative > div.ph5.pb5 > div.org-top-card__primary-content.org-top-card-primary-content--zero-height-logo.org-top-card__improved-primary-content--ia > div.block.mt2 > div > p').text.strip()
        # if description:
        #     print("Description: " + description.text.strip())
    except Exception as e:
        print(e)

    try:
        industry = soup.select_one('* > div.relative > div.ph5.pb5 > div.org-top-card__primary-content.org-top-card-primary-content--zero-height-logo.org-top-card__improved-primary-content--ia > div.block.mt2 > div > div > div.org-top-card-summary-info-list__info-item').text.strip()
        # if industry:
        #     print("Indsutry: " + industry.text.strip())
    except Exception as e:
        print(e)

    try:
        location = soup.select_one('* > div.relative > div.ph5.pb5 > div.org-top-card__primary-content.org-top-card-primary-content--zero-height-logo.org-top-card__improved-primary-content--ia > div.block.mt2 > div > div > div.inline-block > div:nth-child(1)').text.strip()
        # if location:
        #     print("Location: " + location)
    except Exception as e:
        print(e)

    return name, description, location, industry
