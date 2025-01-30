import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import csv

degrees = pd.read_csv(os.path.join("polished_data", "degrees.csv"))

# plt.hist(degrees['Undirected degree'], bins=100, log=True)
# plt.hist(degrees['In-degree'], bins=100, log=True)
# plt.hist(degrees['Out-degree'], bins=100, log=True)
# plt.show()

x, counts = np.unique(degrees["Undirected degree"].to_numpy(), return_counts=True)

frequencies = counts / degrees.shape[0]
kmin = 2
kmax = 2000
gamma = 1 + 1 / np.mean(
    np.log(
        degrees.loc[
            (degrees["Undirected degree"] >= kmin)
            & (degrees["Undirected degree"] <= kmax),
            "Undirected degree",
        ].to_numpy()
        / kmin
    )
)
C = (
    (gamma - 1)
    / (kmin ** (1 - gamma))
    * degrees.loc[
        (degrees["Undirected degree"] >= kmin) & (degrees["Undirected degree"] <= kmax),
        "Undirected degree",
    ].sum()
    / degrees["Undirected degree"].sum()
)

print(f"{C=}")

# degrees.loc[degrees['Undirected degree'] >= 100].sort_values(by=['Undirected degree', 'Name'], ascending=False).to_csv(
#     os.path.join('polished_data', 'high_degree.csv'), index=False, quoting=csv.QUOTE_NONNUMERIC)

plt.loglog(x, frequencies, "o")
plt.loglog([C * k ** (-gamma) for k in range(1, 201)])
plt.show()

# print(np.array([1 + 1 / np.mean(np.log(degrees.loc[degrees['Undirected degree'] >= i, 'Undirected degree'].to_numpy() / i)) for i in range(1,101)]))

# print(f'{gamma=}')
