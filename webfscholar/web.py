from webfscholar import bibtex
from jinja2 import Template
from pathlib import Path
import os
import json


PATH_OUT = 'index.html'
PATH_TEMPLATES = Path(os.path.dirname(os.path.realpath(__file__))) / 'templates'
THEMES = {
    'montserrat-badges': 'montserrat-badges.html'
}


def add_parser(subparsers, parent):
    parser_web = subparsers.add_parser('web', parents=[parent])
    parser_web.add_argument('--theme', choices=THEMES.keys(), default='montserrat-badges')


def compare_year(pub):
    if 'year' in pub:
        return int(pub['year'])
    else:
        # If there's no year, it probably isn't very important, put it at the end.
        print("WARNING: No publication date is available, this item may not sort properly.")
        print("\t" + pub['title'])
        return 0

def main(args):
    db = bibtex.get_bibtex(args)
    if not db.preambles:
        db = bibtex.get_bibtex(args, force_reset=True)

    with open(PATH_TEMPLATES / THEMES[getattr(args, 'theme', 'montserrat-badges')]) as f:
        template = Template(f.read())

    metadata = json.loads(db.preambles[0])
    name = metadata['name']
    publications = db.entries

    publications.sort(key=compare_year, reverse=True)
    for publication in publications:
        publication['author'] = publication['author'] \
            .replace(' and ', ', ') \
            .replace(name, f'<b>{name}</b>')

    out = template.render(publications=publications)
    with open(PATH_OUT, 'w') as f:
        f.write(out)

    print(f'Webpage written to {PATH_OUT}. Open in browser to preview.')
