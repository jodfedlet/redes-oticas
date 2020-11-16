import os
import shutil
import csv
import json
import itertools

REAL_TOPOLOGIES_DIR = 'TopologiasRedesReais'
TOPOLOGIES_DIR = 'Topologias'
MAX_ITERATION = 2


def valid_link(source, target, existing_links):
    return existing_links.isdisjoint(set(itertools.permutations((source, target))))


def get_json_file_name(original_file_name, index, counter):
    return (
        f'{TOPOLOGIES_DIR}/'
        f'{original_file_name.replace(".csv", f"_{index}_{counter}.json")}'
    )


def save_json_file(content, file_name, index='', counter=''):
    with open(get_json_file_name(file_name, index, counter), 'w') as f:
        json.dump(content, f)


def generate_topologies_with_one_more_link(node_list, link_list):
    existing_links = set([(link['From'], link['To'])
                          for link in link_list])
    node_name_list = [node['Id'] for node in node_list]
    for source, target in itertools.combinations(node_name_list, 2):
        if valid_link(source, target, existing_links):
            yield link_list + [{'From': source, 'To': target}]


def get_nodes_and_links_from_csv_file(nodes_file_name):
    link_file_name = nodes_file_name.replace('nodes', 'links')
    with open(f'{REAL_TOPOLOGIES_DIR}/{nodes_file_name}') as nodes_file, \
            open(f'{REAL_TOPOLOGIES_DIR}/{link_file_name}') as links_file:
        node_list = list(csv.DictReader(nodes_file))
        link_list = [{'From': link['From'], 'To': link['To']}
                     for link in csv.DictReader(links_file)]
        return node_list, link_list


def generate_topology_from(node_list, link_list, links_file_name, index, counters):
    if index > MAX_ITERATION:
        return

    counters.setdefault(index, 0)
    for new_link_list in generate_topologies_with_one_more_link(node_list, link_list):
        save_json_file(new_link_list, links_file_name, index, counters[index])
        counters[index] += 1
        generate_topology_from(node_list, link_list,
                               links_file_name, index + 1, counters)


def generate_topologies_from_csv_files():
    for file_name in os.listdir(REAL_TOPOLOGIES_DIR):
        if file_name.endswith('nodes.csv'):
            print(file_name.replace('_nodes.csv', ''))
            links_file_name = file_name.replace('nodes', 'links')
            node_list, link_list = get_nodes_and_links_from_csv_file(file_name)
            generate_topology_from(node_list, link_list,
                                   links_file_name, 1, {})
            save_json_file(node_list, file_name)
            save_json_file(link_list, links_file_name)


if __name__ == '__main__':
    if os.path.exists(TOPOLOGIES_DIR):
        shutil.rmtree(TOPOLOGIES_DIR)

    os.mkdir(TOPOLOGIES_DIR)
    print('Generating...')
    generate_topologies_from_csv_files()
    print('Done')
