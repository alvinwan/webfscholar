from webfscholar import bibtex
from jinja2 import Template
from pathlib import Path
import os
import json


PATH_TEMPLATES = Path(os.getcwd()) / 'templates'
THEMES = {
    'montserrat-badges': 'montserrat-badges.html'
}


def add_parser(subparsers, parent):
    parser_web = subparsers.add_parser('web', parents=[parent])
    parser_web.add_argument('--theme', choices=THEMES.keys(), default='montserrat-badges')


def main(args):
    db = bibtex.get_bibtex(args)

    with open(PATH_TEMPLATES / THEMES[getattr(args, 'theme', 'montserrat-badges')]) as f:
        template = Template(f.read())

    metadata = json.loads(db.preambles[0])
    name = metadata['name']
    publications = db.entries

    for publication in publications:
        publication['author'] = publication['author'] \
            .replace(' and ', ', ') \
            .replace(name, f'<b>{name}</b>')

    out = template.render(publications=publications)
    with open('index.html', 'w') as f:
        f.write(out)

    print('Webpage written to index.html. Open in browser to preview.')
