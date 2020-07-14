from webfscholar import bibtex
from jinja2 import Template
from pathlib import Path


PATH_TEMPLATES = Path('webfscholar/templates')
THEMES = {
    'montserrat-badges': 'montserrat-badges.html'
}


def add_parser(subparsers, parent):
    parser_web = subparsers.add_parser('web', parents=[parent])
    parser_web.add_argument('--theme', choices=THEMES.keys(), default='montserrat-badges')
    parser_web.add_argument('--search', action='store_true', help='Include search bar')


def main(args):
    db = bibtex.get_bibtex(args)

    with open(PATH_TEMPLATES / THEMES[args.theme]) as f:
        template = Template(f.read())

    out = template.render(publications=db.entries)
    with open('index.html', 'w') as f:
        f.write(out)
