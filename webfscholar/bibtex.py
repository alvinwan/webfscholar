"""Populate local bibtex"""


from scholarly import scholarly
from webfscholar import config
from tqdm import tqdm


PATH_BIBTEX = "references.bib"


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
