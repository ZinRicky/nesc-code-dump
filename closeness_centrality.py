import pandas as pd
import numpy as np
import scipy.sparse as spsp
import os

edges = pd.read_csv(os.path.join('polished_data', 'comment_graph.csv'))

node: str = 'ballerinafarm'

# print(edges.loc[(edges.Target == node) | (edges.Source == node), 'Weight'].sum()) # THIS IS WRONG!