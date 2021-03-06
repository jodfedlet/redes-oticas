import os
import json
import itertools
from datetime import date, datetime
from functools import reduce

import networkx as nx
from networkx.algorithms.connectivity import build_auxiliary_edge_connectivity
from networkx.algorithms.flow import build_residual_network


def get_link_index(u, v):
    return tuple(sorted([u, v]))


def first_fit(spectrum_list):
    for i in range(len(nodes)):
        if sum([s[i] for s in spectrum_list]) == 0:
            return i
    return -1


def find_color(spectrum_list):
    possibleColors = {i for i in range(1, len(nodes) + 1)}
    usedColors = reduce(
        lambda prev, value: prev.union(value),
        map(set, spectrum_list),
        set(),
    )
    try:
        return min(list(possibleColors - usedColors))
    except ValueError:
        return -1


def node_list_to_link_list(node_list):
    return [(node_list[i], node_list[i + 1]) for i in range(len(node_list) - 1)]


def rsa(source, target, index):
    shortest_path_as_link_list = node_list_to_link_list(
        shortest_paths[source][target][index]
    )
    spectrum_list = [
        spectrum_dict[get_link_index(u, v)] for u, v in shortest_path_as_link_list
    ]
    ff = first_fit(spectrum_list)
    if ff == -1:
        return False
    for u, v in shortest_path_as_link_list:
        spectrum_dict[get_link_index(u, v)][ff] = ff + 1

    return True


block_rate_dict = {}
for filename in filter(
    lambda filename: filename.endswith("nodes.json"), os.listdir("Topologias")
):
    with open(f"Topologias/{filename}", "r") as nodes_file:
        index = 0
        nodes = list(map(lambda node: node["Id"], json.load(nodes_file)))
        demands = list(itertools.combinations(nodes, 2))
        while True:
            try:
                links_file_name = filename.replace("nodes", "links_" + str(index))
                with open(f"Topologias/{links_file_name}") as links_file:
                    print(links_file_name)
                    links = list(
                        map(
                            lambda link: (link["From"], link["To"]),
                            json.load(links_file),
                        )
                    )
                    graph = nx.Graph()
                    graph.add_nodes_from(nodes)
                    graph.add_edges_from(links)

                    spectrum_dict = {
                        get_link_index(u, v): [0] * len(nodes) for u, v in links
                    }
                    shortest_paths = {}

                    before = datetime.now()
                    H = build_auxiliary_edge_connectivity(graph)
                    R = build_residual_network(H, "capacity")

                    for u in nodes:
                        shortest_paths[u] = {
                            v: sorted(nx.edge_disjoint_paths(graph, u, v, auxiliary=H, residual=R), key=len)[:2]
                            for v in nodes
                            if u != v
                        }
                    after = datetime.now()
                    print('Shortest paths:', after - before)

                    def get_number_of_blocks():
                        return sum(
                            [
                                1 if not (rsa(*demand, 0) and rsa(*demand, 1)) else 0
                                for demand in demands
                            ]
                        )


                    before = datetime.now()
                    block_rate_dict[links_file_name] = get_number_of_blocks() / len(
                        demands
                    )
                    after = datetime.now()

                    print('Block rate:', after - before)

                    index += 1
            except Exception as error:
                break

json.dump(block_rate_dict, open("block_rates.json", "w"))
