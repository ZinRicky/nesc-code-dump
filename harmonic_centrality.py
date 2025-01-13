import pandas as pd
import numpy as np
import scipy.sparse as spsp
import os
# from collections import deque
from typing import Any
from tqdm import tqdm

edges = pd.read_csv(os.path.join('polished_data', 'comment_graph.csv'))
# additional = None
# for source in edges.Source:
#     for target in edges.loc[edges.Source == source]['Target']:
#         if edges.loc[(edges.Source == target) & (edges.Target == source)].empty:
#             new_row = pd.DataFrame([{'Source': target, 'Target': source, 'Weight': edges.loc[(
#                     edges.Source == target) & (edges.Target == source), 'Weight'].values[0]}])
#             if additional is None:
#                 additional = new_row.copy()
#             else:
#                 additional = pd.concat((additional, new_row))
# edges = pd.concat((edges, additional))


node: str = 'gwenthemilkmaid'

harmonic_centrality = .0

starting_nodes = set(edges.Source)
distances: dict[str, dict[str, Any]] = dict()

for y in tqdm(starting_nodes, position=tqdm._get_free_pos(), leave=False):
    distances[y] = dict()
    Q = []
    for n in starting_nodes:
        distances[y][n] = np.inf
        Q.append(n)
    distances[y][y] = .0
    # Q = Q[:20]
    # if node not in Q:
    #     Q.append(node)

    while node in Q:
        w, u = min([(distances[y][n], n) for n in Q])
        Q.remove(u)
        # print(f'{len(Q)=}')
        neighbours = edges.loc[edges.Source == u, 'Target']
        for v in tqdm(neighbours, position=tqdm._get_free_pos(), leave=False):
            if v in Q:
                alt = w + 1 / edges.loc[(edges.Source == u) & (edges.Target == v), 'Weight'].squeeze()
                if alt < distances[y][v]:
                    distances[y][v] = alt

    harmonic_centrality += 1 / distances[y][node]

print(f'{harmonic_centrality=}')