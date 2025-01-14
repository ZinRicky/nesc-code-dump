import numpy as np
import pandas as pd
import scipy.sparse as spsp
import os
import re
from collections import defaultdict
from tqdm import tqdm
import csv

raw_nodes: set = set()
edges = pd.read_csv(os.path.join('polished_data', 'comment_graph.csv'))

print("Indexing source nodes.")
for x in tqdm(edges.Source):
    raw_nodes.add(x)

print("Indexing target nodes.")
for x in tqdm(edges.Target):
    raw_nodes.add(x)

nodes: list = list(raw_nodes)
nodes_number = len(nodes)
nodes_dict: dict[str, int] = {x: i for i,x in enumerate(nodes)}

with open(os.path.join('polished_data', 'nodes.txt'), 'w', encoding='utf-8') as fp:
    for node in nodes:
        fp.write(node + '\n')


# print(f'{nodes_number=}')
unnormalised_adjacency_matrix = spsp.coo_array(
    (nodes_number, nodes_number), dtype=np.float32)

print("Creating adjacency matrix.")
for edge in tqdm(edges.itertuples(), total=edges.shape[0]):
    x = edge.Source
    y = edge.Target
    w = edge.Weight

    j = nodes_dict[x]
    i = nodes_dict[y]
    unnormalised_adjacency_matrix += spsp.coo_array(
        ([w], ([i], [j])), shape=(nodes_number, nodes_number), dtype=np.float32)

unnormalised_adjacency_matrix = unnormalised_adjacency_matrix.tocsr()

adjacency_matrix = spsp.coo_array(
    unnormalised_adjacency_matrix.shape, dtype=np.float32)

print("Normalising adjacency matrix.")
for i, x in tqdm(enumerate(unnormalised_adjacency_matrix.transpose()), total=unnormalised_adjacency_matrix.shape[0]):
    N = x.sum()
    if N:
        adjacency_matrix += spsp.coo_array(
            (x.data / N, ([i for y in x.indices], x.indices)), shape=adjacency_matrix.shape, dtype=np.float32)

adjacency_matrix = adjacency_matrix.transpose()

spsp.save_npz(os.path.join('polished_data',
              'comment_adjacency_matrix.npz'), adjacency_matrix)
