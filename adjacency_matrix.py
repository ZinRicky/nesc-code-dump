import numpy as np
import pandas as pd
from scipy.sparse import coo_array, save_npz
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
print(f'{nodes_number=}')
adjacency_matrix = coo_array((nodes_number, nodes_number), dtype=np.float32)

print("Creating adjacency matrix")
for edge in tqdm(edges.itertuples(), total=edges.shape[0]):
    x = edge.Source
    y = edge.Target
    w = edge.Weight

    j = nodes.index(x)
    i = nodes.index(y)
    adjacency_matrix += coo_array(([w], ([i], [j])),
                                  shape=(nodes_number, nodes_number), dtype=np.float32)

save_npz(os.path.join('polished_data', 'comment_adjacency_matrix_unnormalised.npz'), adjacency_matrix)