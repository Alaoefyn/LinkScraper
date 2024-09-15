import requests
from bs4 import BeautifulSoup
import re
import json
import csv

def fetch_html_with_fallback(url):
    headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        },
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        },
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; AS; AS; rv:11.0) like Gecko'
        }
    ]

    for header in headers:
        try:
            response = requests.get(url, headers=header)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching URL {url} with headers {header}: {e}")
            continue

    return None

def filter_links(html, whitelist, blacklist, regex_pattern, include_domains, exclude_domains):
    if html is None:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]

    if regex_pattern:
        links = regex_filter(links, regex_pattern)

    filtered_links = []
    for link in links:
        if any(domain in link for domain in exclude_domains):
            continue
        if include_domains and not any(domain in link for domain in include_domains):
            continue
        if any(kw in link.lower() for kw in whitelist):
            filtered_links.append(link)
        elif not any(kw in link.lower() for kw in blacklist):
            filtered_links.append(link)

    return filtered_links

def export_links(links, filename, format):
    if format == 'csv':
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Link'])
            for link in links:
                writer.writerow([link])
    elif format == 'json':
        with open(filename, 'w') as jsonfile:
            json.dump(links, jsonfile, indent=4)

def regex_filter(links, pattern):
    regex = re.compile(pattern)
    return [link for link in links if regex.search(link)]
