#! /usr/bin/env python

import xml.etree.ElementTree as ET
from subprocess import Popen, PIPE

input_fn = 'INPUT-findbugs.xml'
output_fn = 'findbugs-remarkup.xml'

tree = ET.parse(input_fn)

items = tree.findall('BugPattern[@type]')


def convert_body(body):
    pandoc = Popen(['pandoc', '--from=html', '--to=remarkup.lua'],
                   stdin=PIPE, stdout=PIPE)
    stdout, stderr = pandoc.communicate(body)
    if pandoc.wait():
        raise Exception('Pandoc exited non-zero')
    return stdout.decode('UTF-8')

output = ET.Element("findbugs")
for item in items:
    name = item.get('type')
    body = item.find('Details').text
    body = convert_body(body)
    body = '\n' + body + '\n'

    ET.SubElement(output, 'BugPattern', name=name).text = body

tree = ET.ElementTree(output)
tree.write(output_fn, encoding='utf-8')
