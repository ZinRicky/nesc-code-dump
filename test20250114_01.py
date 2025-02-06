import scipy.sparse as spsp
import numpy as np
import os

M = spsp.load_npz(
    os.path.join("polished_data", "influencer_adjacency_matrix_via_comments.npz")
)

print(M.sum())
