import numpy as np
import pandas as pd
from tqdm import tqdm
import os
import csv
from collections import defaultdict


def default_list():
    return [0, 0]


df = pd.read_csv("polished_data/non_people_light_edges_list.csv")
node_degrees: defaultdict[str, int] = defaultdict(int)
degrees: defaultdict[str, list] = defaultdict(default_list)
names: set[str] = set()

for edge in tqdm(df.itertuples(), total=df.shape[0]):
    names.add(edge.Source)
    names.add(edge.Target)

    degrees[edge.Source][1] += 1
    degrees[edge.Target][0] += 1

names_list: list[str] = list(names)

pd.DataFrame(
    {
        "Name": names_list,
        "Undirected degree": [sum(degrees[name]) for name in names_list],
        "In-degree": [degrees[name][0] for name in names_list],
        "Out-degree": [degrees[name][1] for name in names_list],
    }
).sort_values(by="Undirected degree", ascending=False).to_csv(
    os.path.join("polished_data", "non_people_light_degrees.csv"),
    index=False,
    quoting=csv.QUOTE_MINIMAL,
)
