import networkx as nx
import os
import json

from networkx.readwrite import json_graph

path_to_json = './Topologias'

json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json') and not pos_json.endswith('nodes.json')]

with open('./wienerIndexes.json', 'w') as wienerIndexes:

    wienerIndexesDict = {}

    for fileName in json_files:
            with open('./Topologias/' + fileName, 'r') as json_file:

                JSONLinks = json.load(json_file)

                G = nx.Graph()

                G.add_weighted_edges_from(
                    (elem['From'], elem['To'], 1)
                    for elem in JSONLinks
                )

                wienerIndex = nx.wiener_index(G)

                wienerIndexesDict[fileName] = wienerIndex

    json.dump(wienerIndexesDict, wienerIndexes)

# G.add_nodes_from(
#     elem['From']
#     for elem in JSONLinks
# )

# G.add_edges_from(
#     (elem['From'], elem['To'])
#     for elem in JSONLinks
# )

# print(G)

# wienerIndex = nx.wiener_index(G)

# # nx.draw(
# #     G,
# #     with_labels=True
# # )

# print(wienerIndex)