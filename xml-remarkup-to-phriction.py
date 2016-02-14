#! /usr/bin/env python

# Converts the output of other scripts into a single Phriction page.
# mostly useful for verifying the results are valid remarkup.

import sys
import xml.etree.ElementTree as ET
from subprocess import Popen, PIPE
import json

phriction_slug = '/'
phab_api = 'http://127.0.0.1:8080/api/'
title = u'Translated Messages'

if not phab_api:
    print 'Specify phab_api'
    sys.exit(4)

input_fn = 'findbugs-remarkup.xml'

tree = ET.parse(input_fn)
root = tree.getroot()


content = [u'= ' + title]

for item in root:
    tag = item.tag
    name = item.get('name')
    body = item.text

    content += [
        '== //%s// %s' % (tag, name),
        body,
        '',
    ]

content = u'\n'.join(content)
params = {
    'slug': phriction_slug,
    'title': title,
    'content': content
}
params = json.dumps(params)
arc = Popen(
    ['arc', '--conduit-uri', phab_api, 'call-conduit', 'phriction.edit'],
    stdin=PIPE, stdout=PIPE)
arc.communicate(params)
