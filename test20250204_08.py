import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import csv

degrees = pd.read_csv(os.path.join("polished_data", "full_degrees.csv"))

# fig1, ax = plt.subplots()
# # plt.hist(degrees["Undirected degree"], bins=100, log=True, color="#5e82b6")
# # plt.hist(degrees["In-degree"], bins=100, log=True, color="#e19c24")
# plt.hist(degrees["Out-degree"], bins=100, log=True, color="#8fb132")
# # fig1.legend(["Undirected", "In", "Out"])
# # ax.set_xlim(left=1)
# # ax.set_xscale("log")
# ax.set_xlabel("Out-bound degree")
# ax.set_ylabel("Count")
# plt.show()

x, counts = np.unique(degrees["Out-degree"].to_numpy(), return_counts=True)

frequencies = counts / degrees.shape[0]
kmin = 10
# kmax = np.inf
gamma = 1 + 1 / np.mean(
    np.log(
        degrees.loc[
            (degrees["Out-degree"] >= kmin),
            "Out-degree",
        ].to_numpy()
        / kmin
    )
)

# C = (gamma - 1) * kmin ** (1 - gamma)
# gamma = 2.5
C = 0.3

print(f"{gamma=}")
print(f"{C=}")

fig1, ax = plt.subplots()
(f2,) = ax.loglog(
    [1, 201],
    [C * k ** (-gamma) for k in [1, 200]],
    color="#101010",
    ls="--",
    label=f"Power law ($\\gamma = {gamma:.3f}$)",
)
(f1,) = ax.loglog(x[x != 0], frequencies[x != 0], "o", color="#8fb132", label="Data")
# ax.set_ylim(top=0.1)
ax.legend(handles=[f1, f2])
ax.set_xlabel("Degree $k$")
ax.set_ylabel("$p_k$")
ax.set_ylim(bottom=5e-7)
plt.show()
