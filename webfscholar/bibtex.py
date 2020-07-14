"""Populate local bibtex"""

from scholarly import scholarly
from webfscholar import config, profile
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
    publications = profile.get_publications(config.get_author_id(args))
    
    bib = []
    for i, publication in enumerate(publications):
        publication['ENTRYTYPE'] = publication.get('ENTRYTYPE', 'article')
        publication['ID'] = publication.get('ID', str(i))
        bib.append(bibtexparser.dumps(publication))

    with open(PATH_BIBTEX, "w") as f:
        for item in bib:
            f.write(item + "\n")
    print(f"Saved {len(bib)} bibtex entries to {PATH_BIBTEX}")
