import pandas as pd
import os
from collections import defaultdict
import csv
from tqdm import tqdm

node_degrees: defaultdict[str, int] = defaultdict(int)
edges = pd.read_csv(os.path.join("polished_data", "comment_graph.csv"))

for edge in tqdm(edges.itertuples(), total=edges.shape[0]):
    node_degrees[edge.Target] += int(edge.Weight)

with open(
    os.path.join("polished_data", "in_degree.csv"), "w", encoding="utf-8", newline=""
) as fp:
    file_writer = csv.writer(fp, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    file_writer.writerow(["Label", "In-degree"])
    for x in node_degrees:
        file_writer.writerow([x, node_degrees[x]])
