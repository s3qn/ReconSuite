import argparse
import re
import requests
from collections import Counter as cnt
from bs4 import BeautifulSoup as bs

# Get HTML Page
def get_html(url):
    try:
        r_site = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Error: Site is invalid, exiting...")
        exit(1)

    if r_site.status_code != 200:
        print("Error: Bad HTTP response. exiting...")
        exit(1)
    return r_site.text

# BeautifulSoup Parsing
def parse_words_from_html(url):
    html = get_html(url)
    soup = bs(html, 'html.parser')
    soup_text = soup.get_text()
    soup_words = re.findall(r'\w+', soup_text.lower())
    return soup_words

# Filter Length
def filter_length(url, min_length):
    soup_words = parse_words_from_html(url)
    filtered_words = []
    for word in soup_words:
        if len(word) < min_length:
            continue
        else:
            filtered_words.append(word)
    return filtered_words

# Count words with collections
def count_words(url, min_length):
    filtered_words = filter_length(url, min_length)
    count_list = cnt(filtered_words)
    return count_list

# Main Guard Block ( to avoid code being imported )
def main():

    # Parser Arguments
    parser = argparse.ArgumentParser(description="Custom word extractor!")
    parser.add_argument("-u", "--url", required=False, default='https://larch-networks.com', help="URL to scan for words")
    parser.add_argument("-l", "--length", required=False, default=0, type=int, help="minimum word length")
    args = parser.parse_args()

    # Main Function
    site = args.url
    length = args.length
    print(f'''--- Common word analyzer ---
    Scanning Link: {site} for common words!
    ''')
    if length > 0:
        print(f'''    Filtering words that are shorter than {length} characters!''')
    top_words = count_words(site, length)
    # Print out the 10 most common words
    print(f'''
    Most common word: "{top_words.most_common(1)[0][0].capitalize()}"
    Top 10 most common words:
    ''')
    for word, count in top_words.most_common(10):
        print(f'"{word.capitalize()}" found {count} times!')


if __name__ == '__main__':
    main()