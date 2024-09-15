import re

def regex_filter(links, pattern):
    regex = re.compile(pattern)
    return [link for link in links if regex.search(link)]
