import numpy as np
import pandas as pd
import networkx as nx
from scipy.stats import linregress
import matplotlib.pyplot as plt
from tqdm import tqdm

df = pd.read_csv("polished_data/people_edges_list.csv")
all_people = nx.from_pandas_edgelist(df, "Source", "Target", "Weight")

number_of_neighbours = all_people.degree()
average_neighbours_degree = []
for i in tqdm(nx.nodes(all_people)):
    my_sum = 0
    for j in nx.neighbors(all_people, i):
        my_sum += number_of_neighbours[j]
    average_neighbours_degree.append(my_sum / number_of_neighbours[i])

list_of_degree = np.array([all_people.degree(i) for i in nx.nodes(all_people)])
average_neighbours_degree = np.array(average_neighbours_degree)

# ZONA REGRESSIONE LINEARE
from scipy.stats import linregress

# low_degs = [x for x in np.unique(list_of_degree) if x <= 100]
avg_average = np.array(
    [
        average_neighbours_degree[list_of_degree == i].mean()
        for i in np.unique(list_of_degree)
    ]
)
lin_reg = linregress(np.log(np.unique(list_of_degree)), np.log(avg_average))

fig1, ax = plt.subplots()
# plt.figure(figsize=(30,30))
ax.loglog(list_of_degree, average_neighbours_degree, "o")
ax.loglog(np.unique(list_of_degree), avg_average, "o", color="#fea030")
ax.loglog(
    [list_of_degree.min(), list_of_degree.max()],
    np.exp(lin_reg.intercept)
    * np.array([list_of_degree.min(), list_of_degree.max()]) ** lin_reg.slope,
    label="Average",
    color="#101010",
    ls="--",
)
ax.set_xlabel("Degree")
ax.set_ylabel("Average Neighbour Degree")
ax.set_title("Assortativity plot")
ax.legend()
ax.set_ylim(bottom=0.9)
plt.show()
