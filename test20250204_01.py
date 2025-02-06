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

x, counts = np.unique(degrees["In-degree"].to_numpy(), return_counts=True)

frequencies = counts / degrees.shape[0]
kmin = 3
gamma = 1 + 1 / np.mean(
    np.log(
        degrees.loc[
            (degrees["In-degree"] >= kmin),
            "In-degree",
        ].to_numpy()
        / kmin
    )
)

# C = (
#     degrees.loc[
#         (degrees["In-degree"] >= kmin),
#         "In-degree",
#     ].sum()
#     / degrees["In-degree"].sum()
# )

C = (gamma - 1) * kmin ** (1 - gamma)

print(f"{gamma=}")
print(f"{C=}")

# degrees.loc[degrees['Undirected degree'] >= 100].sort_values(by=['Undirected degree', 'Name'], ascending=False).to_csv(
#     os.path.join('polished_data', 'high_degree.csv'), index=False, quoting=csv.QUOTE_NONNUMERIC)
fig1, ax = plt.subplots()
ax.loglog(x, frequencies, "o")
ax.loglog(range(kmin, 201), [C * k ** (-gamma) for k in range(kmin, 201)])
ax.set_ylim(top=0.1)
plt.show()

# print(np.array([1 + 1 / np.mean(np.log(degrees.loc[degrees['Undirected degree'] >= i, 'Undirected degree'].to_numpy() / i)) for i in range(1,101)]))

# print(f'{gamma=}')
