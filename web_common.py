from urllib.parse import urlparse

def company_url_specific_comparasion(company_url):
    if company_url.startswith('https://www.linkedin.com/company/'):
        if company_url.endswith('/jobs/') or company_url.endswith('/about/') or company_url.endswith('/people/'):
            return True

    return False

def normalize_company_url(company_url):
    return company_url.replace('/people/', '/').replace('/jobs/', '/').replace('/about/', '/')

def extract_home_link(url):
    # Assuming url is a string variable containing the URL
    # Split the URL by "/" to separate different parts
    parts = url.split("/")

    # Extract the domain part (the second part after the protocol)
    # Assuming the URL format is "http://example.com/career-page"
    domain = parts[2]

    # Construct the home link using the protocol and domain
    home_link = f"{parts[0]}//{domain}/"

    return home_link

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
