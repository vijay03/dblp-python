import requests
from lxml import etree
from collections import namedtuple

DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
DBLP_AUTHOR_SEARCH_URL = DBLP_BASE_URL + 'search/author'

DBLP_PERSON_URL = DBLP_BASE_URL + 'pers/xk/{urlpt}'
DBLP_PUBLICATION_URL = DBLP_BASE_URL + 'rec/bibtex/{key}.xml'

DBLP_VENUE_URL = DBLP_BASE_URL + 'pers/xk/{urlpt}'
DBLP_PUB_SEARCH_URL = DBLP_BASE_URL + 'search/publ/api'

class LazyAPIData(object):
    def __init__(self, lazy_attrs):
        self.lazy_attrs = set(lazy_attrs)
        self.data = None

    def __getattr__(self, key):
        if key in self.lazy_attrs:
            if self.data is None:
                self.load_data()
            return self.data[key]
        raise AttributeError, key

    def load_data(self):
        pass

class Author(LazyAPIData):
    """
    Represents a DBLP author. All data but the author's key is lazily loaded.
    Fields that aren't provided by the underlying XML are None.

    Attributes:
    name - the author's primary name record
    publications - a list of lazy-loaded Publications results by this author
    homepages - a list of author homepage URLs
    homonyms - a list of author aliases
    """
    def __init__(self, urlpt):
        self.urlpt = urlpt
        self.xml = None
        super(Author, self).__init__(['name','publications','homepages',
                                      'homonyms'])

    def load_data(self):
        resp = requests.get(DBLP_PERSON_URL.format(urlpt=self.urlpt))
        # TODO error handling
        xml = resp.content
        self.xml = xml
        root = etree.fromstring(xml)
        data = {
            'name':root.attrib['name'],
            'publications':[Publication(k) for k in 
                            root.xpath('/dblpperson/dblpkey[not(@type)]/text()')],
            'homepages':root.xpath(
                '/dblpperson/dblpkey[@type="person record"]/text()'),
            'homonyms':root.xpath('/dblpperson/homonym/text()')
        }

        self.data = data

def first_or_none(seq):
    try:
        return next(iter(seq))
    except StopIteration:
        pass

Publisher = namedtuple('Publisher', ['name', 'href'])
Series = namedtuple('Series', ['text','href'])
Citation = namedtuple('Citation', ['reference','label'])

class Publication(LazyAPIData):
    """
    Represents a DBLP publication- eg, article, inproceedings, etc. All data but
    the key is lazily loaded. Fields that aren't provided by the underlying XML
    are None.

    Attributes:
    type - the publication type, eg "article", "inproceedings", "proceedings",
    "incollection", "book", "phdthesis", "mastersthessis"
    sub_type - further type information, if provided- eg, "encyclopedia entry",
    "informal publication", "survey"
    title - the title of the work
    authors - a list of author names
    journal - the journal the work was published in, if applicable
    volume - the volume, if applicable
    number - the number, if applicable
    chapter - the chapter, if this work is part of a book or otherwise
    applicable
    pages - the page numbers of the work, if applicable
    isbn - the ISBN for works that have them
    ee - an ee URL
    crossref - a crossrel relative URL
    publisher - the publisher, returned as a (name, href) named tuple
    citations - a list of (text, label) named tuples representing cited works
    series - a (text, href) named tuple describing the containing series, if
    applicable
    """
    def __init__(self, key):
        self.key = key
        self.xml = None
        super(Publication, self).__init__( ['type', 'sub_type',
                                            'mdate', 'authors',
                                            'editors', 'title',
                                            'year', 'month',
                                            'journal', 'venue',
                                            'volume', 'number',
                                            'chapter', 'pages', 'ee',
                                            'isbn', 'url',
                                            'booktitle', 'crossref',
                                            'publisher', 'school',
                                            'citations', 'series'])

    def load_data(self):
        resp = requests.get(DBLP_PUBLICATION_URL.format(key=self.key))
        xml = resp.content
        self.xml = xml
        root = etree.fromstring(xml)
        publication = first_or_none(root.xpath('/dblp/*[1]'))
        if publication is None:
            raise ValueError
        data = {
            'type':publication.tag,
            'sub_type':publication.attrib.get('publtype', None),
            'mdate':publication.attrib.get('mdate', None),
            'authors':publication.xpath('author/text()'),
            'editors':publication.xpath('editor/text()'),
            'title':first_or_none(publication.xpath('title/text()')),
            'year':int(first_or_none(publication.xpath('year/text()'))),
            'month':first_or_none(publication.xpath('month/text()')),
            'journal':first_or_none(publication.xpath('journal/text()')),
            'venue':first_or_none(publication.xpath('venue/text()')),
            'volume':first_or_none(publication.xpath('volume/text()')),
            'number':first_or_none(publication.xpath('number/text()')),
            'chapter':first_or_none(publication.xpath('chapter/text()')),
            'pages':first_or_none(publication.xpath('pages/text()')),
            'ee':first_or_none(publication.xpath('ee/text()')),
            'isbn':first_or_none(publication.xpath('isbn/text()')),
            'url':first_or_none(publication.xpath('url/text()')),
            'booktitle':first_or_none(publication.xpath('booktitle/text()')),
            'crossref':first_or_none(publication.xpath('crossref/text()')),
            'publisher':first_or_none(publication.xpath('publisher/text()')),
            'school':first_or_none(publication.xpath('school/text()')),
            'citations':[Citation(c.text, c.attrib.get('label',None))
                         for c in publication.xpath('cite') if c.text != '...'],
            'series':first_or_none(Series(s.text, s.attrib.get('href', None))
                      for s in publication.xpath('series'))
        }

        self.data = data

def search(author_str):
    resp = requests.get(DBLP_AUTHOR_SEARCH_URL, params={'xauthor':author_str})
    #TODO error handling
    root = etree.fromstring(resp.content)
    return [Author(urlpt) for urlpt in root.xpath('/authors/author/@urlpt')]

def searchvenue(venue_str):
    resp = requests.get(DBLP_PUB_SEARCH_URL, params={'q':venue_str})
    #TODO error handling
    root = etree.fromstring(resp.content)
    return [Publication(url) for url in root.xpath('//info/key/text()')]

def getvenueauthors(venue_str, venue_short):
    resp = requests.get(DBLP_PUB_SEARCH_URL, params={'q':venue_str, 'h':100})
    #TODO error handling
    root = etree.fromstring(resp.content)
    ans = []
    for x in root.findall(".//info/[venue='" + venue_short + "']/../"):
        ptext = [y.text for y in x.findall("./pages")]
        ttext = [y.text for y in x.findall(".title")]
        # Ignore proceedings
        if ttext and "Proceedings" in ttext[0]:
            continue
        # If there is no page information, add all entries anyway
        if not ptext:
            ans.extend([y.text for y in x.findall("./authors/author")])
        if ptext:
            if "-" in ptext[0]:
                a, b = ptext[0].split("-")
                if (int(b) - int(a)) > 5:
                    ans.extend([y.text for y in x.findall("./authors/author")])
    return ans

def getvenueauthorsbypaper(venue_str, venue_short):
    resp = requests.get(DBLP_PUB_SEARCH_URL, params={'q':venue_str, 'h':1000})
    #TODO error handling
    root = etree.fromstring(resp.content)
    ans = []
    each_ans = []
    for x in root.findall(".//info/[venue='" + venue_short + "']/../"):
        ptext = [y.text for y in x.findall("./pages")]
        ttext = [y.text for y in x.findall(".title")]
        # Ignore proceedings
        if ttext and "Proceedings" in ttext[0]:
            continue
        # If there is no page information, add all entries anyway
        if not ptext:
            each_ans = [y.text for y in x.findall("./authors/author")]
        if ptext:
            if "-" in ptext[0]:
                a, b = ptext[0].split("-")
                if (int(b) - int(a)) > 5:
                    each_ans = [y.text for y in x.findall("./authors/author")]

        if len(each_ans) > 0:
            ans.append(each_ans)
                    
    return ans
