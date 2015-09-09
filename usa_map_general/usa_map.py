# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import csv
import sys, os
import shapefile
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.collections import LineCollection
from matplotlib.patches import PathPatch
from matplotlib.font_manager import FontProperties

curdir = sys.path[0] + '/'

mpl.rcParams['font.family'] = 'sans-serif'

thisblue = '#23238e'
fig = plt.figure(figsize=(11.7, 8.3))

plt.subplots_adjust(
    left=0.05, right=0.95, top=0.95, bottom=0.05, wspace=0.15, hspace=0.05)
ax = plt.subplot(111)

x1 = -128.
x2 = -63.5
y1 = 24
y2 = 51

m = Basemap(resolution='i', projection='merc', llcrnrlat=y1,
            urcrnrlat=y2, llcrnrlon=x1, urcrnrlon=x2)

m.fillcontinents(color='0.8')
m.drawmapboundary(fill_color= thisblue)



m.drawparallels(np.arange(y1, y2, 5.), labels=[
                1, 0, 0, 0], color='black', labelstyle='+/-', linewidth=0.2)  # draw parallels
m.drawmeridians(np.arange(x1, x2, 5.), labels=[
                0, 0, 0, 1], color='black', labelstyle='+/-', linewidth=0.2)  # draw meridians



r = shapefile.Reader(curdir + "USA_adm1")
shapes = r.shapes()
records = r.records()




cnt = 0
for record, shape in zip(records, shapes):
    print(cnt)

    lons,lats = zip(*shape.points)
    data = np.array(m(lons, lats)).T

    if len(shape.parts) == 1:
        segs = [data,]
    else:
        segs = []
        for i in range(1,len(shape.parts)):
            index = shape.parts[i-1]
            index2 = shape.parts[i]
            segs.append(data[index:index2])
        segs.append(data[index2:])

    lines = LineCollection(segs,antialiaseds=(1,))
    lines.set_facecolors(np.random.rand(3, 1) * 0.5 + 0.5)
    lines.set_edgecolors('k')
    lines.set_linewidth(0.1)
    ax.add_collection(lines)
    cnt += 1


infile = open(curdir +'state_info_revised.csv','r')
csvfile = csv.reader(infile)



for lakepoly in m.lakepolygons:
    lp = Polygon(lakepoly.boundary, zorder=3)
    lp.set_facecolor(thisblue)
    lp.set_linewidth(0.1)
    ax.add_patch(lp)


for line in csvfile:
    lon = (float(line[0]) + float(line[2]))/2 + float(line[5])
    lat = (float(line[1]) + float(line[3]))/2 + float(line[6])
    x, y = m(lon, lat)
    name = line[4].replace('\\n', '\n')
    plt.text(x, y, name, horizontalalignment='center', verticalalignment='center', fontsize=int(line[7]))

xx, yy = m(-72.0, 26.0)
plt.text(xx, yy, u'Made by zhyuey', color='yellow')

plt.title('Map of contiguous United States', fontsize=24)

# plt.savefig('usa_state_75.png', dpi=75)
# plt.savefig('usa_state_75.png', dpi=75)
plt.savefig('usa_state_300.png', dpi=300)
# plt.savefig('usa_state_600.png', dpi=600)


