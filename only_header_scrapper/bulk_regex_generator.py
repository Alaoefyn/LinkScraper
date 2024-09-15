import re

def generate_bulk_regex_patterns(urls):
    patterns = []
    for url in urls:
        try:
            # Extract base domain and path
            base_domain_pattern = r'https?://(?:www\.)?([a-z0-9]+)\.([a-z]{2,})(?:\.[a-z]{2})?'
            match = re.match(base_domain_pattern, url)
            
            if match:
                domain = match.group(1)
                tld = match.group(2)
                
                # Remove base URL part
                base_url = f"https://{domain}.{tld}"
                path = re.sub(r'^https?://(?:www\.)?' + re.escape(domain) + r'\.' + re.escape(tld) + '/', '', url)
                
                # Escape special regex characters in path
                path = re.escape(path)
                
                # Handle hyphens separately if needed
                path = path.replace(r'\-', '-')
                
                # Create regex pattern
                if url.endswith('/'):
                    regex_pattern = f"^https?://(?:[a-z]+\.)?{re.escape(domain)}\.{re.escape(tld)}/{path}.*$"
                else:
                    regex_pattern = f"^https?://(?:[a-z]+\.)?{re.escape(domain)}\.{re.escape(tld)}/{path}.*$"
                
                patterns.append(regex_pattern)
            else:
                patterns.append(f'Invalid URL format: {url}')
        except Exception as e:
            patterns.append(f'Error processing URL {url}: {str(e)}')

    return patterns
