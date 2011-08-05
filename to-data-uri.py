#!/usr/bin/python

import sys
import html5lib
import base64
from urlparse import urljoin
from urllib2 import urlopen

cache = {}
base_href = None

def to_data_url(url):
  if base_href:
    url = urljoin(base_href, url)
  if url not in cache:
    try:
      f = urlopen(url)
      sys.stderr.write("Download %s ... " % url)
      sys.stderr.flush()
      cache[url] = "data:%s;base64,%s" % (
        f.info()
          .getheader("Content-Type")
          .replace('; charset=', ';charset='),
        base64.urlsafe_b64encode(f.read()))
      sys.stderr.write("ok\n")
    except:
      sys.stderr.write("Link to %s\n" % url)
      cache[url] = url
  return cache[url]

def main():
  f = sys.stdin
  doc = html5lib.parse(f, treebuilder="lxml", namespaceHTMLElements=False)
  e = doc.findall("/html/head/base[@href]")
  if e:
    base_href = e.get('href')
  for e in doc.findall("//*[@src]"):
    e.set('src', to_data_url(e.get('src')))
  doc.write(sys.stdout, method="html")

if __name__ == '__main__':
  main()
  
