#!/usr/bin/env python3


from bs4 import BeautifulSoup as page
from curses import wrapper
import curses
import requests
import sys
import time


stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)


def parse_args_to_query():
    if len(sys.argv) == 1:
        print('Usage: wiki <your search as separate strings>')
        print('\n')

    elif len(sys.argv) > 1:
        query = sys.argv[1].capitalize()

    if len(sys.argv) > 2:
        for arg in sys.argv[2:]:
            if arg != ('the' or 'an' or 'and' or 'or' or 'in' or 'on'):
                print(arg)
                arg = arg.capitalize()
                print(arg)
                query += '_'
                query += arg

    return query


def get_page(url):
    res = requests.get(url)
    return res.text


def map_DOM(webpage):
    webpage = page(webpage, 'html.parser')
    return webpage


def is_valid_wiki_query(webpage):
    check = webpage.find(id='noarticletext')
    if check is None:
        return True
    else:
        return False


def isolate_content(webpage):
    content_container = webpage.find(id='mw-content-text')
    return content_container


def get_paragraphs(content):
    paragraphs = content.find_all('p')
    return paragraphs


def clean_paragraphs(paragraphs):
    clean_paragraphs = []
    for p in paragraphs:
        p = p.get_text()
        if p != '':
            clean_paragraphs.append(p)
        else:
            pass
    return clean_paragraphs


def paragraph_list():
    query_string = parse_args_to_query()
    print(query_string)
    raw_page = get_page('https://en.wikipedia.org/wiki/' + query_string)
    mapped_page = map_DOM(raw_page)
    if is_valid_wiki_query(mapped_page):
        content = isolate_content(mapped_page)
        target_text = get_paragraphs(content)
        display_text = clean_paragraphs(target_text)
        return display_text
    else:
        print(query_string + 'Try different capitalization')
        sys.exit(1)


def get_links(content):
    links = []
    for link in content.find_all('a'):
        links.append(link)
    return links


def get_all_js(webpage):
    scripts = []
    for script in webpage.find_all('script'):
        source = script.get('src')
        if source is not None:
            scripts.append(source)
    return scripts


def teardown():
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.endwin()


def main(stdscr):
    paragraphs = paragraph_list()
    p_count = len(paragraphs)
    current_p = 0
    stdscr.nodelay(True)
    stdscr.clear()

    while True:
        c = stdscr.getch()
        curses.flushinp()
        stdscr.clear()
        stdscr.addstr(paragraphs[current_p])
        stdscr.refresh()

        if c == curses.KEY_DOWN and current_p < (p_count - 1):
            current_p += 1
        elif c == curses.KEY_UP and current_p > 0:
            current_p -= 1
        elif c == ord('q'):
            teardown()
            sys.exit()

        time.sleep(0.05)


wrapper(main)

if __name__ == '__main__':
    main()
