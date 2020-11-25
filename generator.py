import os
import shutil
import csv
import json
import itertools
import random


REAL_TOPOLOGIES_DIR = 'TopologiasRedesReais'
TOPOLOGIES_DIR = 'Topologias'


def valid_link(link, existing_links):
    source, target = map(lambda l: l['Id'], link)
    existing_links_set = {(l['From'], l['To']) for l in existing_links}
    return existing_links_set.isdisjoint(set(itertools.permutations((source, target))))


def save_json_file(content, file_name):
    with open(f'{TOPOLOGIES_DIR}/{file_name}.json', 'w') as f:
        json.dump(content, f)


def get_nodes_and_links_from_csv_file(nodes_file_name, link_file_name):
    with open(f'{REAL_TOPOLOGIES_DIR}/{nodes_file_name}.csv') as nodes_file, \
            open(f'{REAL_TOPOLOGIES_DIR}/{link_file_name}.csv') as links_file:
        node_list = list(csv.DictReader(nodes_file))
        link_list = [{'From': link['From'], 'To': link['To']}
                     for link in csv.DictReader(links_file)]
        return node_list, link_list


def add_random_link_to_link_list(node_list, link_list):
    possible_links = list(itertools.combinations(node_list, 2))
    random.shuffle(possible_links)
    if len(link_list) < len(possible_links):
        for link in possible_links:
            if valid_link(link, link_list):
                link_list.append({'From': link[0]['Id'], 'To': link[1]['Id']})
                break
        return True
    return False


def generate_topology_from(node_list, link_list, links_file_name, number_of_links_added):
    graph_avg_degree = (len(link_list) * 2) / len(node_list)
    if graph_avg_degree < 5 and add_random_link_to_link_list(node_list, link_list):
        save_json_file(
            link_list, f'{links_file_name}_{number_of_links_added + 1}')
        generate_topology_from(node_list, link_list,
                               links_file_name, number_of_links_added + 1)


def generate_topologies_from_csv_files():
    for nodes_file_name in filter(lambda file_name: file_name.endswith('nodes.csv'), os.listdir(REAL_TOPOLOGIES_DIR)):
        print(nodes_file_name.replace('_nodes.csv', ''))
        nodes_file_name = nodes_file_name.replace('.csv', '')
        links_file_name = nodes_file_name.replace('nodes', 'links')
        node_list, link_list = get_nodes_and_links_from_csv_file(
            nodes_file_name, links_file_name)
        save_json_file(node_list, nodes_file_name)
        save_json_file(link_list, links_file_name)
        generate_topology_from(node_list, link_list,
                               links_file_name, 0)


if __name__ == '__main__':
    if os.path.exists(TOPOLOGIES_DIR):
        print('Removing existing folder...')
        shutil.rmtree(TOPOLOGIES_DIR)

    os.mkdir(TOPOLOGIES_DIR)
    print('Generating...')
    generate_topologies_from_csv_files()
    print('Done')
