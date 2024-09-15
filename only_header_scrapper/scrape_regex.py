import re

def test_regex(pattern, test_string):
    try:
        # Compile the regex pattern
        regex = re.compile(pattern)
        
        # Find all matches in the test string
        matches = regex.findall(test_string)
        
        return matches

    except re.error as e:
        raise RuntimeError(f'Invalid regex pattern: {str(e)}')
