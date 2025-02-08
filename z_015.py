import numpy as np
import pandas as pd
from tqdm import tqdm

df = pd.read_csv("polished_data/hashtags_edges_list_undirected.csv")
raw_nodes: set = set()

print("Indexing source nodes.")
for x in tqdm(df.Source):
    raw_nodes.add(x)

print("Indexing target nodes.")
for x in tqdm(df.Target):
    raw_nodes.add(x)

print(f"{len(raw_nodes)=}")
print(f"{df.shape[0]=}")
