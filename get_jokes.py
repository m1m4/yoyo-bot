import urllib.request
import os
import json

from bs4 import BeautifulSoup

url = 'http://jokes.yo-yoo.co.il/?'
PATH = os.path.dirname(os.path.realpath(__file__)) + r'\jokes'
jokes_mapping = json.loads(open(PATH + r'\dict.json', 'r').read())


def extract_jokes(cat_key, page):
    print(f'        Requesting {url}cat={cat_key}&page={page}... ')
    page = urllib.request.urlopen(url + f'cat={cat_key}&page={page}').read()
    soup = BeautifulSoup(page, 'html.parser')

    table = soup.find('table', {'width': '1320'})
    div_contents = table.find('tr').find_all('td')[1].find_all('div')

    jokes_nofilter = list()

    for div in div_contents:
        d = div.get_text().strip()
        jokes_nofilter.append(d.split('\n'))

    jokes = list()
    for i in range(4, len(jokes_nofilter), 6):
        jokes.append(" ".join(jokes_nofilter[i]))

    return jokes


def download_category_jokes(cat):
    jokes = extract_jokes(jokes_mapping.get(cat), 1)

    file = open(PATH + rf'\jokes-{cat}.txt', 'wb')

    for joke in jokes:
        file.write((joke + '\n').encode())

    file.close()

    file = open(PATH + rf'\jokes-{cat}.txt', 'ab')

    print(f'    Finished page 1 in {cat}')

    for i in range(2, 17):
        jokes = extract_jokes(jokes_mapping.get(cat), i)

        for joke in jokes:
            file.write((joke + '\n').encode())

        print(f'    Finished page {i} in {cat}')

    file.close()
    print(f'Finished {cat} jokes')


def main():
    for cat in jokes_mapping:
        download_category_jokes(cat)


# def main():
#
#     jokes = extract_jokes(1)
#
#     file = open(PATH + r'\joke.txt', 'wb')
#
#     for joke in jokes:
#         file.write((joke + '\n').encode())
#
#     file.close()
#
#     file = open(PATH + r'\joke.txt', 'ab')
#
#     print('Finished page 1')
#
#     for i in range(2, 17):
#         jokes = extract_jokes(i)
#
#         for joke in jokes:
#             file.write((joke + '\n').encode())
#
#         print(f'Finished page {i}')


if __name__ == '__main__':
    main()
