"""
Parse and paginate publications on user profile (which usually have conference name)
"""

from bs4 import BeautifulSoup
import requests


def get_publications(author_id, start=0, length=100):
    response = requests.get(
        f'https://scholar.google.com/citations?user={author_id}&hl=en&cstart={start}&pagesize={length}')
    soup = BeautifulSoup(response.text, features='html.parser')

    publications = []
    for soup_ in soup.findAll(class_='gsc_a_tr')[2:]:  # first two are [empty, header]
        content = soup_.findAll(class_='gs_gray')
        publication = {
            "title": soup_.find(class_='gsc_a_at').text,
            "author": content[0].text,
            "citations": int(soup_.find(class_='gsc_a_ac').text or 0)
        }

        year = soup_.find(class_='gs_oph')
        if year:
            publication["year"] = int(year.text.replace(", ", ""))

        journal = content[1].contents
        if journal:
            journal = journal[0]
            if "," in journal:
                journal, pages = journal.split(",", 1)
                publication["pages"] = pages
            publication["journal"] = journal

        publications.append(publication)
    return publications
