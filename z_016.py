import numpy as np
import pandas as pd
from tqdm import tqdm
import os
import csv
from collections import defaultdict


def default_list():
    return [0, 0]


df = pd.read_csv(os.path.join("polished_data", "hashtags_edges_list_undirected.csv"))
names = pd.read_csv(
    os.path.join("polished_data", "hashtags_from_influencers.csv")
).Hashtag.tolist()
# ht_names = set(names.Name)


degrees: defaultdict[str, list] = defaultdict(default_list)

for edge in tqdm(df.itertuples(), total=df.shape[0]):
    degrees[edge.Source][1] += 1
    degrees[edge.Target][0] += 1

pd.DataFrame(
    {
        "Name": names,
        "In-degree": [degrees[name][0] for name in names],
        "Out-degree": [degrees[name][1] for name in names],
    }
).sort_values(by="In-degree", ascending=False).to_csv(
    os.path.join("polished_data", "hashtags_degrees.csv"),
    index=False,
    quoting=csv.QUOTE_MINIMAL,
)
