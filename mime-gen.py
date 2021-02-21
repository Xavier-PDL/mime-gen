# Author: Xavier Ponce de Leon
# File: mime-gen.py
# Description: Scrape mozilla developer reference for HTTP MIME types and
# generate a python file containing a dictionary with extensions as keys along
# with its MIME type as its value.
#
# For example:
#   File extension: .aac
#   MIME-type: audio/aac
#   Dict entry: '.aac': 'audio/aac'
#

import requests
from bs4 import BeautifulSoup, element

url = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types"

r = requests.get(url)
html = r.content.decode()

soup = BeautifulSoup(html, "html.parser")

tableRows = soup.find_all('tr')

extMime = {}

for row in tableRows:
    exts = []
    mime = []
    columnCount = 0
    for item in row.contents:
        if item == '\n':
            continue
        for itemContents in item.contents:
            if itemContents.name == 'code':
                if columnCount == 0:
                    if itemContents.string is None:
                        for elem in itemContents.contents:
                            if type(elem) is element.NavigableString:
                                exts.append(str(elem).strip())
                    else:
                        exts.append(itemContents.string)
                elif columnCount == 2:
                    mime.append(itemContents.string)
            elif itemContents.name == 'p':
                mime.append(itemContents.code.string)
            else:
                continue
        columnCount += 1
    if len(exts) == 0:
        continue
    else:
        for ext in exts:
            extMime[ext] = mime[0]

testDict = {
        'key': 'value',
        'key2': 'value2'
}

dictLen = len(extMime) - 1
with open("mimeTypes.py", "w") as f:
    f.write("# Generated by mime-gen.py\n")
    f.write("mimeDict = {\n")
    for key in extMime.keys():
        if dictLen > 0:
            f.write("    '{}': '{}',\n".format(key, extMime[key]))
        else:
            f.write("    '{}': '{}'\n".format(key, extMime[key]))
        dictLen -= 1
    f.write("}\n")
