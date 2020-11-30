import csv
import itertools
from typing import List, Dict, Tuple, TypedDict, Optional

import networkx as nx

Node = str
NodeList = List[Node]
Edge = Tuple[Node, Node]
EdgeList = List[Edge]


def node_list_to_edge_list(nodes: NodeList):
    return [(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)]


def reverse_edges_from_source_to_target(g: nx.DiGraph, shortest_path: EdgeList):
    for u, v in shortest_path:
        g.remove_edge(u, v)
        g[v][u]["weight"] = 0


def get_edge_disjoint_shortest_paths(
    g: nx.Graph,
    source: Node,
    target: Node,
    shortest_paths: Dict[Node, EdgeList],
    ws: Dict[Node, int],
    t: nx.Graph,
):
    print(source, target)
    for edge in g.edges(data=True):
        edge[2]["weight"] = 1 - ws[edge[0]] + ws[edge[1]]

    reverse_edges_from_source_to_target(g, shortest_paths[target])

    return None


def get_all_pairs_edge_disjoint_shortest_paths(g: nx.DiGraph):
    edge_disjoint_shortest_paths = {}

    for source in g.nodes:
        shortest_paths = {
            target: node_list_to_edge_list(path)
            for target, path in nx.shortest_path(g, source, weight="weight").items()
        }
        ws = {node: len(shortest_paths[node]) for node in g.nodes}
        t = nx.DiGraph()
        t.add_nodes_from(g.nodes)
        t.add_edges_from(
            itertools.chain(
                *map(lambda path: node_list_to_edge_list(path), shortest_paths.values())
            )
        )
        for target in g.nodes:
            edge_disjoint_shortest_paths[source] = (
                target,
                get_edge_disjoint_shortest_paths(
                    g.copy().to_directed(),
                    source,
                    target,
                    shortest_paths,
                    ws,
                    t.to_directed(),
                ),
            )

    return edge_disjoint_shortest_paths


graph = nx.Graph()


with open("TopologiasRedesReais/scteste_nodes.csv") as nf:
    with open("TopologiasRedesReais/scteste_links.csv") as ef:
        nodes = list(map(lambda n: n["Id"], csv.DictReader(nf)))
        edges = list(map(lambda e: (e["From"], e["To"], 1), csv.DictReader(ef)))
        graph.add_nodes_from(nodes)
        graph.add_weighted_edges_from(edges)
        print(nx.wiener_index(graph, weight='weight'))

# get_all_pairs_edge_disjoint_shortest_paths(graph.to_directed())


# graph = nx.Graph()
# graph.add_nodes_from(["s", "a", "b", "c", "d", "e", "f", "g"])
# graph.add_edges_from(
#     [
#         ("s", "a"),
#         ("s", "b"),
#         ("s", "d"),
#         ("a", "c"),
#         ("a", "d"),
#         ("a", "e"),
#         ("b", "e"),
#         ("c", "f"),
#         ("d", "f"),
#         ("e", "g"),
#         ("f", "g"),
#     ]
# )

# graph = graph.to_directed()
# ws = nx.shortest_path_length(graph, 'a')
# t = nx.shortest_path(graph, 'a')



# get_edge_disjoint_shortest_paths(graph.to_directed(), 's', 'f')