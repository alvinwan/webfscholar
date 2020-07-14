"""Populate local bibtex"""

from scholarly import scholarly
from webfscholar import config, profile
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import bibtexparser
from tqdm import tqdm
import json
import os


PATH_BIBTEX = "references.bib"


def get_bibtex(args):
    if getattr(args, 'reset', False):
        main(args)
    if not os.path.exists(PATH_BIBTEX):
        main(args)
    with open(PATH_BIBTEX) as f:
        return bibtexparser.load(f)


def add_parser(subparsers, parent):
    parser_build = subparsers.add_parser('bibtex', parents=[parent])


def main(args):
    publications, name = profile.get_publications(config.get_author_id(args))

    for i, publication in tqdm(enumerate(publications)):
        publication['ENTRYTYPE'] = publication.get('ENTRYTYPE', 'article')
        publication['ID'] = publication.get('ID', str(i))

    db = BibDatabase()
    db.entries = publications
    db.preambles = [json.dumps({"name": name})]

    writer = BibTexWriter()
    with open(PATH_BIBTEX, "w") as f:
        f.write(writer.write(db))
    print(f"Saved {len(publications)} bibtex entries to {PATH_BIBTEX}")
