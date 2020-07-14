from configparser import ConfigParser
from scholarly import scholarly
import itertools
import questionary

PATH_CONFIG = "config.ini"


def get_author_id(args):
    if get_cfg('main.id') is None or args.reset:
        main(args)
    return get_cfg('main.id')


def search_author(batch_size=10):
    name = questionary.text("Search for yourself (name, institution):").ask()
    query = scholarly.search_author(name)
    authors = list(itertools.islice(query, batch_size))

    if len(authors) > 0:
        return pick_author(query, authors, batch_size)
    if len(authors) == 1:
        return authors[0]
    print('Try again. No authors found.')
    return search_author()


def pick_author(query, authors, batch_size=10):
    index = len(authors)
    choices = [f"{author.name} ({author.email})" for author in authors]

    while index == len(choices):
        if len(choices) == batch_size:
            choices += ["Next"]
        choice = questionary.select("Which one is you?", choices=choices).ask()
        if choice is None:
            return search_author(batch_size)
        index = choices.index(choice)

        if index < batch_size:
            return authors[index]
        authors = list(itertools.islice(query, 10))
        choices = [f"{author.name} ({author.email})" for author in authors]


def cfg():
    config = ConfigParser()
    config.read(PATH_CONFIG)

    if not config.has_section('main'):
        config.add_section('main')
    return config


def get_cfg(fqkey):
    config = cfg()
    section, key = fqkey.split('.', 1)
    if key in config.options(section):
        return config.get(section, key)


def set_cfg(fqkey_to_value):
    config = cfg()
    for fqkey, value in fqkey_to_value.items():
        section, key = fqkey.split('.', 1)
        config.set(section, key, value)
    with open(PATH_CONFIG, 'w') as f:
        config.write(f)


def add_parser(subparsers, parent):
    parser_config = subparsers.add_parser('config', parents=[parent])
    parser_config.add_argument('--set', help='save Google Scholar id')
    parser_config.add_argument('--get', action='store_true', help='get Google Scholar id')


def main(args):
    if getattr(args, 'get', None):
        print(get_cfg(args.key))
        return
    id = getattr(args, 'set', None) or search_author().id
    set_cfg({'main.id': id})
    print(f"Successfully saved author ID {id} to {PATH_CONFIG}")
