import os
import re
import json
import statistics
import functools

from scipy.stats import pearsonr

BLOCK_RATES_FILENAME = 'block_rates.json'
WIENER_INDEXES_FILENAME = 'wienerIndexes.json'

block_rate = json.load(open(BLOCK_RATES_FILENAME, 'r'))
wiener_indexes = json.load(open(WIENER_INDEXES_FILENAME, 'r'))

block_rate_list = []
wiener_indexes_list = []


def repl(value, prev):
    prev.add(re.sub(r'_links_\d*\.json', '', value))
    return prev


network_names = functools.reduce(
    lambda prev, value: repl(value, prev), block_rate.keys(), set())


def get_values_of(name, v_dict):
    return list(map(lambda v: v_dict[v], filter(
        lambda value: value.startswith(name), sorted(v_dict.keys()))))


corr_list = []

for name in network_names:
    xs = get_values_of(name, wiener_indexes)
    ys = get_values_of(name, block_rate)
    corr, _ = pearsonr(xs, ys)
    corr_list.append((name, abs(corr)))
    print(f'Correlação de {name}: {corr}')


for key in sorted(block_rate.keys()):

    block_rate_list.append(block_rate[key])
    wiener_indexes_list.append(wiener_indexes[key])

print(f'Correlação geral: {pearsonr(wiener_indexes_list, block_rate_list)}')

print(f'Média: {statistics.fmean(map(lambda x: x[1],corr_list))}')

corr_list.sort(key=lambda x: x[1])
bigger = corr_list[-2:]
smaller = corr_list[:2]
print(bigger)
print(smaller)
