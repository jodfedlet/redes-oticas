import json
import itertools

import networkx as nx
import  matplotlib.pyplot as plt 

nodes = list(
    map(lambda node: node["Id"], json.load(open("Topologias/scteste_nodes.json")))
)
links = list(
    map(
        lambda link: (link["From"], link["To"]),
        json.load(open("Topologias/scteste_links.json")),
    )
)

demands = list(itertools.combinations(nodes, 2))

graph = nx.Graph()
graph.add_nodes_from(nodes)
graph.add_edges_from(links)

for demand in demands:
    smallest_paths = sorted(nx.edge_disjoint_paths(graph, demand[0], demand[1]), key=len)[:2]
