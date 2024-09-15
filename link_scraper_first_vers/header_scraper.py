import requests
from bs4 import BeautifulSoup

def fetch_header_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        header_links = []

        # Adjust the selectors according to the structure of the website you are targeting
        header_sections = soup.select('header, .header, .main-header, .top-header')
        
        for section in header_sections:
            links = section.find_all('a', href=True)
            for link in links:
                href = link['href']
                if not href.startswith('http'):
                    href = requests.compat.urljoin(url, href)
                header_links.append(href)

        return header_links

    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return []
