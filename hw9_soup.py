import requests
from bs4 import BeautifulSoup
import json

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def get_authors(soup):
    authors = []
    for author in soup.select('.author'):
        author_url = url + author.find_next('a')['href']
        author_soup = get_soup(author_url)
        author_info = {
            'fullname': author.text,
            'born_date': author_soup.select('.author-born-date')[0].text,
            'born_location': author_soup.select('.author-born-location')[0].text,
            'description': author_soup.select('.author-description')[0].text.strip()
        }
        if author_info not in authors:
            authors.append(author_info)
    return authors

def get_quotes(soup):
    quotes = []
    for quote in soup.select('.quote'):
        quote_info = {
            'tags': [tag.text for tag in quote.select('.tag')],
            'author': quote.select('.author')[0].text,
            'quote': quote.select('.text')[0].text
        }
        quotes.append(quote_info)
    return quotes

if __name__ == "__main__":

    url = 'http://quotes.toscrape.com'
    print(url)
    soup = get_soup(url)

    authors = get_authors(soup)
    quotes = get_quotes(soup)

    next_page_link = soup.select_one('.next > a')

    while next_page_link:
        print(url + next_page_link['href'])
        soup = get_soup(url + next_page_link['href'])
        new_authors = get_authors(soup)
        for author in new_authors:
            if author not in authors:
                authors.append(author)        
        quotes += get_quotes(soup)
        next_page_link = soup.select_one('.next > a')

    with open('authors.json', 'w', encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=2)

    with open('quotes.json', 'w', encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)
