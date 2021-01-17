import os
import sys
import csv
import json

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import networkx as nx
from geopy.distance import distance

if len(sys.argv) < 3:
    print('Use o commando da seguinte forma:')
    print(f'\tpython {__file__} <nome da rede> <n do arquivo de enlace>')
    sys.exit(1)

scteste_nodes = list(csv.DictReader(
    open(f'TopologiasRedesReais/{sys.argv[1]}_nodes.csv', 'r')))

scteste_links = json.load(
    open(f'Topologias/{sys.argv[1]}_links_{sys.argv[2]}.json', 'r'))

smaller_lat = min(map(lambda v: float(v['Lat']), scteste_nodes))
bigger_lat = max(map(lambda v: float(v['Lat']), scteste_nodes))
smaller_lon = min(map(lambda v: float(v['Long']), scteste_nodes))
bigger_lon = max(map(lambda v: float(v['Long']), scteste_nodes))


center_lat = (smaller_lat + bigger_lat) / 2
center_lon = (smaller_lon + bigger_lon) / 2

width = distance([center_lat, smaller_lon], [
                 center_lat, bigger_lon]).m + 10**6
height = distance([smaller_lat, center_lon], [
                  bigger_lat, center_lon]).m + 10**6

m = Basemap(
    projection='lcc',
    width=width,
    height=height,
    lat_0=center_lat,
    lon_0=center_lon,
    resolution=None)

lats, longs = m(list(map(lambda node: float(node['Long']), scteste_nodes)),
                list(map(lambda node: float(node['Lat']), scteste_nodes)))

pos = {name: [lat, lon] for name, lat, lon in zip(
    map(lambda n: n['Id'], scteste_nodes), lats, longs)}

G = nx.Graph()
G.add_nodes_from(map(lambda node: node['Id'], scteste_nodes))
G.add_edges_from(map(lambda link: [link['From'], link['To']], scteste_links))

nx.draw_networkx(G, pos=pos, with_labels=True,
                 node_size=100, edge_color='#ffaf03', font_size=8, font_color='#fff')

m.bluemarble()
plt.show()
