#
# BaseMap example by geophysique.be
# tutorial 10
import csv
import shapefile
import numpy as np
import matplotlib as mpl
import sys
mpl.use('Agg')
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.collections import LineCollection
from matplotlib.patches import PathPatch

infile = open('state_info_new_revised.csv','r')
csvfile = csv.reader(infile)

r = shapefile.Reader("UScounties")
shapes = r.shapes()
records = r.records()


cnt_total = 0

for line in csvfile:

    print(cnt_total + 1, line[4].replace('\\n', ' '))
    fig = plt.figure(figsize=(11.7, 8.3))
    fig.clear()
    plt.subplots_adjust(
        left=0.05, right=0.95, top=0.95, bottom=0.05, wspace=0.15, hspace=0.05)
    ax = plt.subplot(111)

    lon_range = (float(line[2]) - float(line[0]))
    lat_range = (float(line[3]) - float(line[1]))


    x1 = float(line[0]) - lon_range * 0.10
    x2 = float(line[2]) + lon_range * 0.10
    y1 = float(line[1]) - lat_range * 0.10
    y2 = float(line[3]) + lat_range * 0.10


    m = Basemap(resolution='h', projection='merc', llcrnrlat=y1,
            urcrnrlat=y2, llcrnrlon=x1, urcrnrlon=x2)


    m.drawmapboundary(fill_color='#0000aa')
    m.fillcontinents(color='w', lake_color='#0000aa')
    # m.drawstates(linewidth=0.5)
    m.drawcountries(linewidth=0.5)



    for record, shape in zip(records,shapes):
        if line[8].find(record[3]) > -1:
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

    for lakepoly in m.lakepolygons:
        lp = Polygon(lakepoly.boundary)
        lp.set_facecolor('#0000aa')
        ax.add_patch(lp)


    # m.drawrivers(linewidth=0.5, zorder = 3, color='blue')

    lon = (float(line[0]) + float(line[2]))/2 + float(line[5])
    lat = (float(line[1]) + float(line[3]))/2 + float(line[6])
    x, y = m(lon, lat)
    name = line[4].replace('\\n', '\n')

    plt.text(x, y, name, horizontalalignment='center', verticalalignment='center', fontsize=24)


    filename = sys.path[0] + '/state_img/m_' + line[4] + '.png'
    print(filename)
    plt.savefig(filename, dpi=300)

    cnt_total += 1


