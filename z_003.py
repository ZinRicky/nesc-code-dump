import numpy as np
import pandas as pd
import os
import scipy.sparse as spsp
import csv


def page_rank(A, q, damping=0.85, tol=1e-10):
    M = damping * A
    q_1 = q / np.linalg.norm(q, ord=1) * (1 - damping)
    page_rank_vector = q_1.copy()

    page_rank_old = page_rank_vector.copy()
    enter_in_cycle = False

    while (
        np.linalg.norm(page_rank_vector - page_rank_old, ord=1) > tol
        or not enter_in_cycle
    ):
        enter_in_cycle = True
        page_rank_old = page_rank_vector.copy()
        page_rank_vector = M @ page_rank_vector + q_1
        page_rank_vector /= np.linalg.norm(page_rank_vector, ord=1)
        print(f"{np.linalg.norm(page_rank_vector - page_rank_old, ord=1)=}")

    return page_rank_vector


adjacency_matrix = spsp.load_npz(
    os.path.join("polished_data", "full_adjacency_matrix.npz")
)
influencers = pd.read_csv(os.path.join("polished_data", "influencers.csv"))

with open(os.path.join("polished_data", "full_nodes.txt"), encoding="utf-8") as fp:
    names = []
    for name in fp.readlines():
        names.append(name.replace("\n", ""))

names_set = set(names)
relevant_influencers = influencers.loc[influencers.Name.apply(lambda s: s in names_set)]
tradwives = set(
    relevant_influencers.loc[relevant_influencers.Category == "Tradwife"].Name.array
)
feminists = set(
    relevant_influencers.loc[relevant_influencers.Category == "Feminist"].Name.array
)

q_tradwives = np.array([int(name in tradwives) for name in names], dtype=np.float64)
q_feminists = np.array([int(name in feminists) for name in names], dtype=np.float64)

page_rank_tradwives = page_rank(adjacency_matrix, q_tradwives)
page_rank_feminists = page_rank(adjacency_matrix, q_feminists)

df = pd.DataFrame(
    {
        "id": names,
        "Tradwife PageRank": page_rank_tradwives,
        "Feminist PageRank": page_rank_feminists,
    }
)

df.sort_values(by="Tradwife PageRank", ascending=False).to_csv(
    os.path.join("polished_data", "full_local_page_rank.csv"),
    index=False,
    quoting=csv.QUOTE_NONNUMERIC,
)

df.to_excel(os.path.join("polished_data", "full_local_pagerank.xlsx"), index=False)
