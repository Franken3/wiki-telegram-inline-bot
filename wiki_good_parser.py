import wikipediaapi


def find_me(search):
    wiki_wiki = wikipediaapi.Wikipedia('ru')
    src = search.replace(' ', '_')
    page_py = wiki_wiki.page(f'{src}')
    if not page_py.exists():
        return False, False
    else:
        return page_py.summary.split('\n')[0], page_py.fullurl

