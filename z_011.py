import numpy as np
import pandas as pd
from tqdm import tqdm
import scipy.sparse as spsp
import os

edges = pd.read_csv("polished_data/people_edges_list.csv")
raw_nodes: set = set()

# print(edges.head())

print("Indexing source nodes.")
for x in tqdm(edges.Source):
    raw_nodes.add(x)

print("Indexing target nodes.")
for x in tqdm(edges.Target):
    raw_nodes.add(x)

nodes: list = list(raw_nodes)
nodes_number = len(nodes)
nodes_dict: dict[str, int] = {x: i for i, x in enumerate(nodes)}

pd.DataFrame({"Name": nodes}).to_csv(
    "polished_data/people_transpose_names.csv", index=False
)


# print(f'{nodes_number=}')
# unnormalised_adjacency_matrix = spsp.coo_array(
#     (nodes_number, nodes_number), dtype=np.float32)

weights = []
row_indices = []
column_indices = []

print("Creating adjacency matrix.")
for edge in tqdm(edges.itertuples(), total=edges.shape[0]):
    x1: str = edge.Source
    x2: str = edge.Target
    w: float = edge.Weight

    j = nodes_dict[x1]
    i = nodes_dict[x2]

    weights.append(w)
    row_indices.append(j)
    column_indices.append(i)

unnormalised_adjacency_matrix = spsp.coo_array(
    (weights, (row_indices, column_indices)),
    shape=(nodes_number, nodes_number),
    dtype=np.float64,
)

adjacency_matrix = unnormalised_adjacency_matrix / np.maximum(
    unnormalised_adjacency_matrix.sum(0), np.ones((nodes_number,))
)

spsp.save_npz(
    os.path.join("polished_data", "people_transpose_adjacency_matrix.npz"),
    adjacency_matrix,
)
