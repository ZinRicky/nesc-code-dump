import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import csv
import os

# import time

df = pd.read_csv("polished_data/complete_graph.csv")
list_of_edges = [(x.Source, x.Target, x.Weight) for x in df.itertuples()]

G: nx.DiGraph = nx.DiGraph()
G.add_weighted_edges_from(list_of_edges)

# print(time.strftime("%X", time.localtime()))
test_data = nx.betweenness_centrality(G, weight="weight")
# print(time.strftime("%X", time.localtime()))

with open(os.path.join("polished_data", "full_nodes.txt"), encoding="utf-8") as fp:
    names = []
    for name in fp.readlines():
        names.append(name.replace("\n", ""))

pd.DataFrame({"id": names, "Betweenness": [test_data[x] for x in names]}).sort_values(
    by="Betweenness", ascending=False
).to_csv(
    "polished_data/full_betweenness.csv", index=False, quoting=csv.QUOTE_NONNUMERIC
)

# fig1, ax = plt.subplots()
# ax.loglog(df.Followers, df.PageRank, "o", color="#5e82b6")
# ax.set_xlabel("# followers")
# ax.set_ylabel("PageRank score")
# plt.show()
