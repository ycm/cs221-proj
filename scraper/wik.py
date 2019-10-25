#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup
from subprocess import check_output

URL_BASE = 'https://en.wiktionary.org/wiki/'

def get_pg(c):
    '''
    Pulls a Wiktionary page and retrieves unstructured CJKV info for further cleanup
    '''
    # Pull complete page
    src = check_output([
        'wget',
        '-qO-',
        URL_BASE + c
    ])

    if 'Middle Chinese' not in src.decode('utf-8'):
        return None

    src = BeautifulSoup(src, features='lxml')

    # Titles are <h2>Translingual</h2>, <h2>Japanese</h2>, etc.
    titles = src.findAll('h2')

    if not titles:
        return None

    # FIXME: titles[1:] assumes first <h2> is Contents box. Naive but maybe okay. 
    for title in titles[1:]:
        sp = title.find_all('span')

        try:
            lang = title.next_element['id']
        except TypeError:
            continue
       
        # TODO: Keep pulling next_element until <h2> UNLESS final section. 
        # Find reasonable delimiter for final section.
        curr = title
        for i in range(10):
            print(curr.next_element)
            curr = curr.next_element
        break
        


def main():
    with open(sys.argv[1]) as f:
        chars = [l.strip() for l in f]

    for c in chars:
        # FIXME: 'bad variable name
        contents = get_pg(c)

        if contents is None:
            continue

        break

if __name__ == '__main__':
    main()
