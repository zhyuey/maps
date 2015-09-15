# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import shapefile
import csv

infofile = open('cn_info.csv', 'w')
csvwriter = csv.writer(infofile)

mapreader = shapefile.Reader('CHN_adm1')

records = mapreader.records()
shapes = mapreader.shapes()

fields = mapreader.fields

print(fields)

print(records)

data = []
for lines in records:
	data.append(lines)

csvwriter.writerows(data)