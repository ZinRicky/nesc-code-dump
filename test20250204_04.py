import scipy.sparse as spsp
import numpy as np
import pandas as pd
import os
from tqdm import tqdm
import csv

damping = 0.85
tol = 1e-10

adjacency_matrix = spsp.load_npz(
    os.path.join("polished_data", "full_adjacency_matrix.npz")
)

M = damping * adjacency_matrix
q = (1 - damping) * np.ones((adjacency_matrix.shape[0],)) / adjacency_matrix.shape[0]

# print(f'{q=}')

page_rank_vector = q.copy()

page_rank_old = page_rank_vector.copy()
enter_in_cycle = False

while (
    np.linalg.norm(page_rank_vector - page_rank_old, ord=1) > tol or not enter_in_cycle
):
    enter_in_cycle = True
    page_rank_old = page_rank_vector.copy()
    page_rank_vector = M @ page_rank_vector + q
    page_rank_vector /= np.linalg.norm(page_rank_vector, ord=1)
    print(f"{np.linalg.norm(page_rank_vector - page_rank_old, ord=1)=}")

np.save(os.path.join("polished_data", "page_rank_vector.npy"), page_rank_vector)

with open(os.path.join("polished_data", "full_nodes.txt"), encoding="utf-8") as fp:
    names = []
    for name in fp.readlines():
        names.append(name.replace("\n", ""))

# print(names)

pd.DataFrame({"id": names, "PageRank": page_rank_vector}).sort_values(
    by="PageRank", ascending=False
).to_csv(
    os.path.join("polished_data", "full_page_rank.csv"),
    index=False,
    quoting=csv.QUOTE_NONNUMERIC,
)
