import scipy.sparse as spsp
import numpy as np
import pandas as pd
import os
from tqdm import tqdm

damping = 0.85
tol = 1e-5

unnormalised_adjacency_matrix = spsp.load_npz(os.path.join(
    'polished_data', 'comment_adjacency_matrix_unnormalised.npz'))
adjacency_matrix = spsp.coo_array(
    unnormalised_adjacency_matrix.shape, dtype=np.float32)

for i, x in tqdm(enumerate(unnormalised_adjacency_matrix.transpose()), total=unnormalised_adjacency_matrix.shape[0]):
    N = x.sum()
    if N:
        adjacency_matrix += spsp.coo_array(
            (x.data / N, ([i for y in x.indices], x.indices)), shape=adjacency_matrix.shape, dtype=np.float32)

adjacency_matrix = adjacency_matrix.transpose()

spsp.save_npz(os.path.join('polished_data',
              'comment_adjacency_matrix.npz'), adjacency_matrix)

M = damping * adjacency_matrix
q = (1 - damping) * \
    np.ones((adjacency_matrix.shape[0],)) / adjacency_matrix.shape[0]

# print(f'{q=}')

rng = np.random.default_rng()
page_rank_vector = rng.random((adjacency_matrix.shape[0],))
page_rank_vector /= np.linalg.norm(page_rank_vector, ord=1)

page_rank_old = page_rank_vector.copy()
enter_in_cycle = False

while np.linalg.norm(page_rank_vector - page_rank_old, ord=1) > 1e-5 or not enter_in_cycle:
    enter_in_cycle = True
    page_rank_old = page_rank_vector.copy()
    page_rank_vector = M @ page_rank_vector + q
    # print(f'{np.linalg.norm(page_rank_vector - page_rank_old, ord=1)=}')

np.save(os.path.join('polished_data', 'page_rank_vector.npy'), page_rank_vector)
