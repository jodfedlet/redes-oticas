import re
import json
import statistics
import functools

from scipy.stats import pearsonr
import matplotlib.pyplot as plt

BLOCK_RATES_FILENAME = 'block_rates.json'
WIENER_INDEXES_FILENAME = 'wienerIndexes.json'
GRAPH_DEGREES_FILENAME = 'graphDegres.json'
PRINT_FOLDER = 'prints'

block_rate = json.load(open(BLOCK_RATES_FILENAME, 'r'))
wiener_indexes = json.load(open(WIENER_INDEXES_FILENAME, 'r'))
graph_degrees = json.load(open(GRAPH_DEGREES_FILENAME, 'r'))

block_rate_list = []
wiener_indexes_list = []


def repl(value, prev):
    prev.add(re.sub(r'_links_\d*\.json', '', value))
    return prev


network_names = functools.reduce(
    lambda prev, value: repl(value, prev), block_rate.keys(), set())


def get_values_of(n, v_dict):
    return list(map(lambda v: v_dict[v], filter(
        lambda value: value.startswith(n), sorted(v_dict.keys()))))


corr_list = []


def create_image(name, corr, xs, ys, dgs):
    plt.figure(figsize=(15, 10))
    plt.plot(xs, ys, 'ro')
    plt.xlabel('Índice de Wiener')
    plt.ylabel('Taxa de bloqueio')
    plt.grid(True)
    plt.title(f'{name}  -  {corr:.4f}')
    for idx, dg in enumerate(dgs):
        plt.annotate(f'{dg:.1f}', (xs[idx], ys[idx]))
    plt.savefig(fname=f'{PRINT_FOLDER}/{name}.png')
    plt.close()


print('Creating images')
for name in network_names:
    xs = get_values_of(name, wiener_indexes)
    ys = get_values_of(name, block_rate)
    dgs = get_values_of(name, graph_degrees)
    corr, _ = pearsonr(xs, ys)
    create_image(name, corr, xs, ys, dgs)
    corr_list.append((name, abs(corr)))

for key in sorted(block_rate.keys()):
    block_rate_list.append(block_rate[key])
    wiener_indexes_list.append(wiener_indexes[key])


for name, corr in corr_list:
    print(f'{name:17} => {corr:.08f}')


print(f'Média: {statistics.fmean(map(lambda x: x[1],corr_list))}')

print(f'Correlação geral: {pearsonr(wiener_indexes_list, block_rate_list)[0]}')
