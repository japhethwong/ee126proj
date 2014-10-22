from bs4 import BeautifulSoup
import urllib2
import random
import re

TARGET_CLASS = 'gsc_1usr_name'
RAMCHANDRAN_NAME = 'kannan ramchandran'
RAMCHANDRAN_ID = 'DcV-5RAAAAAJ'
CSV_FILENAME = 'author_id_mapping.csv'

def getCoAuthorsForAuthor(author, n=10):
    author_id = getIdForAuthor(author)
    if (not author_id):
        author_id = RAMCHANDRAN_ID
    coauthor_page = getCoAuthorPageUrl(author_id)
    coauthors = searchPageForCoAuthors(coauthor_page)
    return coauthors if (len(coauthors) < n) else random.sample(coauthors, n)

def getCSVEntryForAuthorAndId(author, author_id):
    return str(author)+','+str(author_id)+'\n'

def getIdForAuthor(author):
    if (author in authors_dict):
        return authors_dict[author]
    else:
        return None

def getCoAuthorPageUrl(id):
    return 'http://scholar.google.com/citations?view_op=list_colleagues&hl=en&user='+str(id)

def searchPageForCoAuthors(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    elements_on_page = soup.find_all('h3')
    authors = []
    for element in elements_on_page:
        checked = extractAuthorInfo(element)
        if (not checked):
            continue
        else:
            author_id, author = checked
            if (author_id not in authors_dict):
                authors_dict[author] = author_id
                with open(CSV_FILENAME, 'a') as f:
                    f.write(getCSVEntryForAuthorAndId(author, author_id))
            authors.append(checked)
    return authors

def extractAuthorInfo(node):
    # true if valid author
    # if true, return (author_id, name)
    # else return None

    # Validate node.
    if 'class' in node and node['class'] != TARGET_CLASS:
        return None

    # Get the associated <a> tag.
    a_node = node.a
    if not a_node:
        return None

    url = a_node['href']
    user_id = re.sub(r'^/citations\?user=([^&]+).*$', r'\1', url)
    author_name = a_node.string.lower()
    return user_id, author_name

authors_dict = {}
authors_dict[RAMCHANDRAN_NAME] = RAMCHANDRAN_ID
with open(CSV_FILENAME, 'w') as f:
    f.write(getCSVEntryForAuthorAndId(RAMCHANDRAN_NAME, RAMCHANDRAN_ID))
