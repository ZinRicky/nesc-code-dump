import networkx as nx
import pandas as pd
import os
from pprint import pprint
import csv

edges = pd.read_csv(os.path.join('polished_data', 'comment_graph.csv'))
list_of_edges = [(x.Source, x.Target, 1 / x.Weight) for x in edges.itertuples()]

G: nx.DiGraph = nx.DiGraph()
G.add_weighted_edges_from(list_of_edges)

test_data = nx.harmonic_centrality(G, distance='weight')

with open(os.path.join('polished_data', 'test_harmonic.csv'), 'w', encoding='utf-8', newline='') as fp:
    file_writer = csv.writer(fp, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    for x in test_data:
        file_writer.writerow([x, test_data[x]])