#scrape_links.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = set()
        
        # definite header sections to scrape
        header_tags = [
            'header', 'nav', 'aside', '.menu', '.navbar', '.header', '.sidebar', 
            'footer', '.footer', '.bottom', '.bottom-links', '.footer-links'
        ]
        
        # sumcheck for header tags and their links
        for tag in header_tags:
            for section in soup.select(tag):
                for link in section.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)
                    if not full_url.startswith(url):  # dodge that links not starting with the base URL
                        continue
                    links.add(full_url)
        
        return sorted(links)

    except Exception as e:
        raise RuntimeError(f'Error: {str(e)}')
