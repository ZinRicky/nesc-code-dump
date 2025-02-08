import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

df = pd.read_csv("polished_data/people_page_rank.csv")

df_head = df.loc[:10000]

lr = linregress(
    np.log(df_head.index.to_numpy() + 1), np.log(df_head.PageRank.to_numpy())
)

fig1, ax = plt.subplots()
(f2,) = ax.loglog(
    [1, df.shape[0] + 1],
    np.exp(lr.intercept) * np.array([1, df.shape[0] + 1]) ** lr.slope,
    color="#101010",
    ls="--",
    lw=1,
    label=f"${np.exp(lr.intercept):.3f} \\cdot \\text{{pos}}^{{{lr.slope:.3f}}}$",
)
(f1,) = ax.loglog(range(1, df.shape[0] + 1), df.PageRank, color="#5e82b6", label="Data")
ax.set_xlabel("Rank position")
ax.set_ylabel("PageRank score")
ax.legend(handles=[f1, f2])
plt.show()
