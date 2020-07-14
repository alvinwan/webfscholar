"""Populate local bibtex"""

from scholarly import scholarly
from webfscholar import config
import bibtexparser
from tqdm import tqdm
import os


PATH_BIBTEX = "references.bib"


def get_bibtex(args):
    if not os.path.exists(PATH_BIBTEX):
        main(args)
    with open(PATH_BIBTEX) as f:
        return bibtexparser.load(f)


def add_parser(subparsers, parent):
    parser_build = subparsers.add_parser('bibtex', parents=[parent])


def main(args):
    author = config.get_author(args)
    author.fill()

    bib = []
    with tqdm(total=len(author.publications)) as pbar:
        for i, publication in enumerate(author.publications):
            pbar.set_description(f"{publication.bib['title'][:20]}")
            publication.bib['ENTRYTYPE'] = publication.bib.get('ENTRYTYPE', 'article')
            publication.bib['ID'] = publication.bib.get('ID', str(i))
            bib.append(publication.bibtex)
            pbar.update(1)

    with open(PATH_BIBTEX, "w") as f:
        for item in bib:
            f.write(item + "\n")
    print(f"Saved {len(bib)} bibtex entries to {PATH_BIBTEX}")
