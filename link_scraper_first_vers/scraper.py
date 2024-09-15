import requests
from bs4 import BeautifulSoup
import re
import json
import csv

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def filter_links(html, whitelist, blacklist, regex_pattern, include_domains, exclude_domains):
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

def save_links_to_file(links, filename):
    with open(f"{filename}.txt", 'a') as file:
        for link in links:
            file.write(link + '\n')

def categorize_links(links):
    categorized_links = {
        'images': [],
        'videos': [],
        'documents': [],
        'others': []
    }
    for link in links:
        if any(ext in link for ext in ['.jpg', '.jpeg', '.png', '.gif']):
            categorized_links['images'].append(link)
        elif any(ext in link for ext in ['.mp4', '.avi', '.mov']):
            categorized_links['videos'].append(link)
        elif any(ext in link for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx']):
            categorized_links['documents'].append(link)
        else:
            categorized_links['others'].append(link)

    return categorized_links

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
