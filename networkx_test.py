import networkx as nx
import pandas as pd
import os
from pprint import pprint
import csv

edges = pd.read_csv(os.path.join("polished_data", "comment_graph.csv"))
list_of_edges = [(x.Source, x.Target, x.Weight) for x in edges.itertuples()][:10000]

G: nx.DiGraph = nx.DiGraph()
G.add_weighted_edges_from(list_of_edges)

test_data = nx.betweenness_centrality(G, weight="weight")

pprint({x: test_data[x] for x in test_data if test_data[x]})
