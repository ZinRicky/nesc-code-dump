import numpy as np
import pandas as pd
from tqdm import tqdm
import os
import csv
from collections import defaultdict


def default_list():
    return [0, 0]


df = pd.read_csv(os.path.join("polished_data", "people_edges_list.csv"))
names = pd.read_csv(os.path.join("polished_data", "people_nodes.csv"))
people_names = set(names.Name.array)


degrees: defaultdict[str, list] = defaultdict(default_list)

for edge in tqdm(df.itertuples(), total=df.shape[0]):
    degrees[edge.Source][1] += 1
    degrees[edge.Target][0] += 1

pd.DataFrame(
    {
        "Name": names.Name.array,
        "In-degree": [degrees[name][0] for name in names.Name.to_numpy()],
        "Out-degree": [degrees[name][1] for name in names.Name.to_numpy()],
    }
).sort_values(by="In-degree", ascending=False).to_csv(
    os.path.join("polished_data", "people_degrees.csv"),
    index=False,
    quoting=csv.QUOTE_MINIMAL,
)
