import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import csv

degrees = pd.read_csv(os.path.join("polished_data", "hashtags_degrees.csv"))

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
kmin = 1
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

C = (gamma - 1) * kmin ** (1 - gamma)
# gamma = 2.5
# C = 0.3
# C = 0.8

print(f"{gamma=}")
print(f"{C=}")

fig1, ax = plt.subplots()
(f2,) = ax.loglog(
    range(1, 201),
    [C * k ** (-gamma) for k in range(1, 201)],
    color="#101010",
    ls="--",
    label=f"Power law ($\\gamma = {gamma:.3f}$)",
)
(f1,) = ax.loglog(x, frequencies, "o", color="#e19c24", label="Data")
ax.legend(handles=[f1, f2])
ax.set_xlabel("In-degree $k_{\\text{in}}$")
ax.set_ylabel("$p_{k_{\\text{in}}}$")
# ax.set_ylim(bottom=1e-6)
plt.show()
