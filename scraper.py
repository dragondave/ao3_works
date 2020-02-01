import requests
import lxml.html
from PyRSS2Gen import RSSItem, RSS2, Guid
import requests_cache
from urllib.parse import urljoin
# from datetime import now
import dateparser

requests_cache.install_cache() # DEBUG ONLY

USER = "kimaracretak"

BASE_URL = "https://archiveofourown.org/users/{}/works".format(USER)

html = requests.get(BASE_URL)

with open("h.html", "w") as f:
    f.write(html.text)

items = []
root = lxml.html.fromstring(html.content)
for work in root.xpath("//li[@class='work blurb group']"):
    for a in work.xpath(".//h4/a"):
        if "/works/" in a.attrib["href"]:
            title = a.text
            link = urljoin(BASE_URL, a.attrib["href"])
            guid = link
        if "rel" in a.attrib:
            author = a.text # NOT COMPLIANT

    description = work.xpath(".//blockquote[@class='userstuff summary']")[0].text_content().strip()
    category = work.xpath(".//a[@class='tag']")[0].text
    try:
        comments = urljoin(BASE_URL, work.xpath(".//dd[@class='comments']/a/@href")[0])
    except Exception:
        comments = None
    pubDate = dateparser.parse(work.xpath(".//p[@class='datetime']")[0].text)
    item = RSSItem(
            title = title,
            link = link,
            description = description,
            guid = Guid(guid),
            pubDate = pubDate,
            comments = comments)
    items.append(item)
    print (title, link, author, description, category,comments, pubDate)
    item = None
    link = None
    description = None
    guid = None
    pubDate = None
    comments = None



rss = RSS2(
        title = "AO3 works of {}".format(USER),
        link = BASE_URL,
        description = "{}'s AO3 works".format(USER),
  #      lastBuildDate = now(),

        items = items
         #   RSSItem(
         #       title = title,
         #       link = link,
         #       description = description,
         #       guid = Guid(guid),
         #       pubDate = pubDate,
         #       # author = author, TODO
         #       # category = category, # TODO fails?
         #       comments = comments)]
        )

rss.write_xml(open("fool.xml", "w"))

