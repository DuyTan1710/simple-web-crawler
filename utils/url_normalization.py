import re

def get_normalized_url(url): # return empty string if not valid url
        if not isinstance(url, str):
            return ''
        # remove the query and anchor link of the url (starting with # or ?)
        pattern = re.compile(r'[#?].*')
        normalized_url = re.sub(pattern, '', url)
        if normalized_url == '':
            return ''
        if normalized_url[-1] == '/':
            return normalized_url[:-1]
        return normalized_url