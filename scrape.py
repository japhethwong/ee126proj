from bs4 import BeautifulSoup
import urllib2
import re

TARGET_CLASS = 'gsc_1usr_name'

authors_dict = {}
authors_dict['kannan ramchandran'] = 'DcV-5RAAAAAJ'

def getIdForAuthor(author):
    if (author in authors_dict):
        return authors_dict[author]
    else:
        return -1

def getCoAuthorsForAuthor(author, n=10):
    author_id = getIdForAuthor(author)
    coauthor_page = getCoAuthorPageUrl(author_id)
    coauthors = searchPageForCoAuthors(coauthor_page)
    return coauthors if (len(coauthors) < n) else coauthors[:n]

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
    author_name = a_node.string
    return user_id, author_name
