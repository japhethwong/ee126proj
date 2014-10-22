from bs4 import BeautifulSoup
import urllib2

SCRAPING_CLASS_NAME = 'gsc_luser_name'

authors_dict = {}
authors_dict['kannan ramchandran'] = ''

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

def searchPageForCoAuthors(url)
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    elements_on_page = soup.find_all('h3')
    authors = []
    for (element in elements_on_page):
        checked = checkFormatOfAuthorElement(element)
        if (not checked):
            continue
        else:
            author_id, author = checked
            if (author_id not in authors_dict):
                authors_dict[author] = author_id
            authors.append(checked)
    return authors

def checkFormatOfAuthorElement(tag):
    #true if valid author.
    #if true, return (author_id, name)
    #else return None
