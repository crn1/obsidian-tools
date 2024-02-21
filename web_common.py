from urllib.parse import urlparse
from lxml import etree

def company_url_specific_comparasion(company_url):
    if company_url.startswith('https://www.linkedin.com/company/'):
        if company_url.endswith('/jobs/') or company_url.endswith('/about/') or company_url.endswith('/people/'):
            return True

    return False

def normalize_company_url(company_url):
    return company_url.replace('/people/', '/').replace('/jobs/', '/').replace('/about/', '/')

def extract_home_link(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Extract the netloc (domain)
    domain = parsed_url.netloc

    # Split the domain by '.' to get the top-level domain and its parent domains
    domain_parts = domain.split('.')

    # Check if the domain has at least two parts (e.g., "example.com")
    if len(domain_parts) >= 2:
        # If the last part is a two-letter top-level domain (e.g., "com", "net", "org")
        if len(domain_parts[-1]) == 2:
            # Return the last two parts joined together (including the top-level domain)
            return '.'.join(domain_parts[-2:])
        else:
            # Otherwise, return the last part (the top-level domain) along with its parent domain
            return '.'.join(domain_parts[-2:])
    else:
        # Return the whole domain if it doesn't have at least two parts
        return domain

def is_valid_url(url):
    try:
        if not url:
            return False

        result = urlparse(url)
        return all([result.scheme, result.netloc])

    except ValueError:
        return False

def get_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: Failed to retrieve HTML. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return ''

def is_valid_xpath(xpath):
    if not isinstance(xpath, str):
        return False

    if xpath.lower() == 'nan':
        return False

    try:
        # Try parsing the XPath expression
        etree.XPath(xpath)
        return True
    except Exception as e:
        print(f'Error for Xpath {xpath}: {e}')
        # If there's a syntax error, return False
        return False
