"""
Parse and paginate publications on user profile (which usually have conference name)
"""

from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import arxiv
import string


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
        f'https://scholar.google.com/citations?user={author_id}&hl=en&cstart={start}&pagesize={length}&sortby=pubdate')
    soup = BeautifulSoup(response.text, features='html.parser')

    name = soup.find(id='gsc_prf_in').text
    divs = soup.findAll(class_='gsc_a_tr')

    publications = []
    with tqdm(total=len(divs)) as pbar:
        for soup_ in divs:  # first two are [empty, header]
            content = soup_.findAll(class_='gs_gray')
            publication = {
                "title": soup_.find(class_='gsc_a_at').text,
                "author": content[0],
                "citations": soup_.find(class_='gsc_a_ac').text or '0',
                "url": 'https://scholar.google.com' + soup_.find(class_='gsc_a_at')['data-href']
            }
            pbar.set_description(publication["title"][:10])

            # parse year
            year = soup_.find(class_='gs_oph')
            if year:
                publication["year"] = year.text.replace(", ", "")

            # parse journal + pages
            journal = content[1].contents
            if journal:
                journal = journal[0]
                if "," in journal:
                    journal, pages = journal.split(",", 1)
                    publication["pages"] = pages
                publication["journal"] = hook_journal(journal)

            # get arxiv data
            if 'arxiv' in publication["journal"].lower():
                id = publication["journal"].lower().replace("arxiv:", "")
                paper = arxiv.query(id_list=[id], max_results=1)[0]
            else:
                query = publication['title']
                paper = arxiv.query(query=query, max_results=1)[0]

            if name in paper['authors']:
                for key in ('id', 'updated', 'published', 'summary'):
                    publication[key] = paper[key]
                publication['author'] = ' and '.join(paper['authors'])
                publication['url'] = paper['pdf_url']

            # parse code
            if 'github.com' in publication["summary"]:
                for token in publication["summary"].split():
                    if 'github.com' in token.lower():
                        break
                if token.strip().endswith('.'):
                    token = token.strip()[:-1]
                publication["code"] = token

            publications.append(publication)
            pbar.update(1)
    return publications, name
