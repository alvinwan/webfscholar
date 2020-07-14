from configparser import ConfigParser
from scholarly import scholarly
import questionary

PATH_CONFIG = "config.ini"


def get_author(args):
    """For use by other scrips"""
    query = get_cfg('main.query')
    if query is None or args.reset:
        main(args)
        query = get_cfg('main.query')
    return next(scholarly.search_author(query))


def generator_prefix(generator, prefix=10):
    """
    >>> generator_prefix(iter(range(2)), 10)
    [0, 1]
    >>> generator_prefix(iter(range(100)), 10)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    results = []
    for i in range(prefix):
        try:
            results.append(next(generator))
        except StopIteration:
            return results
    return results


def author2str(author):
    return f"{author.name} ({author.email})"


def cfg():
    config = ConfigParser()
    config.read(PATH_CONFIG)

    if not config.has_section('main'):
        config.add_section('main')
    return config


def get_cfg(fqkey):
    config = cfg()
    results = []
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


def pick_author():
    name = questionary.text("Search for your Google Scholar profile").ask()
    query = scholarly.search_author(name)

    batch_size = 10
    authors = generator_prefix(query, prefix=batch_size)

    if len(authors) > 1:
        attempts = 1
        while True:
            choices = list(map(author2str, authors))
            if len(choices) == batch_size:
                choices += ["Next"]
            choices += ["Retry Search"]
            choice = questionary.select(
                "Which one is you?",
                choices=choices
            ).ask()
            index = choices.index(choice)
            if index < len(choices) - 1 - int("Next" in choices):
                break
            if index == len(choices) - 1:
                return
            if attempts % 2 == 0:
                print(
                    "Maybe quit the program and retry the search, but with your"
                    " institution in the search query?")
            authors = generator_prefix(query, prefix=batch_size)
            attempts += 1
        author = authors[index]
    elif len(authors) == 1:
        author = authors[0]
    else:
        print("No authors found. Please try again.")
        return

    return author


def add_parser(subparsers, parent):
    parser_config = subparsers.add_parser('config', parents=[parent])


def main(args):
    query = get_cfg('main.query')
    if query and not args.reset:
        print(f"Already configured with {query}. Use --reset to reset.")
        return

    author = None
    while author is None:
        author = pick_author()

    query = author2str(author)
    set_cfg({'main.query': query, 'main.id': author.id})
    print(f"Saved {query} with ID {author.id} to {PATH_CONFIG}.")
