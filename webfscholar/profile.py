"""
Parse and paginate publications on user profile (which usually have conference name)
"""

from bs4 import BeautifulSoup
import requests


# if any of these abbreviations are seen, use them
CONF_ABBREVIATIONS = ('ICRA', 'CVPR', 'ECCV', 'ICCV')



def hook_journal(journal):
    if journal.lower().startswith('arxiv preprint'):
        return journal[len('arxiiv preprint'):]
    if 'Computer Vision and Pattern' in journal and 'IEEE' in journal:
        return 'CVPR'
    if journal.lower().startswith('proceedings of the'):
        return journal[len('proceedings of the'):]

    contains = [abbreviation in journal for abbreviation in CONF_ABBREVIATIONS]
    if any(contains):
        journal = CONF_ABBREVIATIONS[contains.index(True)]
    return journal


def get_publications(author_id, start=0, length=100):
    response = requests.get(
        f'https://scholar.google.com/citations?user={author_id}&hl=en&cstart={start}&pagesize={length}')
    soup = BeautifulSoup(response.text, features='html.parser')

    publications = []
    for soup_ in soup.findAll(class_='gsc_a_tr'):  # first two are [empty, header]
        content = soup_.findAll(class_='gs_gray')
        publication = {
            "title": soup_.find(class_='gsc_a_at').text,
            "author": content[0].text,
            "citations": soup_.find(class_='gsc_a_ac').text or '0'
        }

        year = soup_.find(class_='gs_oph')
        if year:
            publication["year"] = year.text.replace(", ", "")

        journal = content[1].contents
        if journal:
            journal = journal[0]
            if "," in journal:
                journal, pages = journal.split(",", 1)
                publication["pages"] = pages
            publication["journal"] = hook_journal(journal)

        publications.append(publication)
    return publications
