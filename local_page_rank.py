import scipy.sparse as spsp
import numpy as np
import os

damping = 0.85
tol = 1e-5

adjacency_matrix = spsp.load_npz(os.path.join('polished_data', 'comment_adjacency_matrix.npz'))
M = damping * adjacency_matrix

examined_nodes: list[int] = [2500, 5503]
local_page_ranks = None

for node in examined_nodes:
    q = np.zeros((adjacency_matrix.shape[0],))
    q[node] += 1 - damping

    rng = np.random.default_rng()
    page_rank_vector = rng.random((adjacency_matrix.shape[0],))
    page_rank_vector /= np.linalg.norm(page_rank_vector, ord=1)

    page_rank_old = page_rank_vector.copy()
    enter_in_cycle = False

    while np.linalg.norm(page_rank_vector - page_rank_old, ord=1) > 1e-5 or not enter_in_cycle:
        enter_in_cycle = True
        page_rank_old = page_rank_vector.copy()
        page_rank_vector = M @ page_rank_vector + q
        page_rank_vector /= np.linalg.norm(page_rank_vector, ord=1)
    
    if local_page_ranks is None:
        local_page_ranks = np.reshape(page_rank_vector, (1,-1))
    else:
        local_page_ranks = np.vstack((local_page_ranks, np.reshape(page_rank_vector, (1,-1))))

print(np.sum(local_page_ranks, axis=1))