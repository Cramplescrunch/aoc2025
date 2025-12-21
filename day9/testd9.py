# Day9B - coordinate compression, matrix approach.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

D9 = pd.read_csv('test2.txt', header=None)

unique = np.unique(D9[[0, 1]])
factors = np.arange(len(unique))

D9[[0, 1]] = D9[[0, 1]].replace(unique, factors)

x = list(D9[0])
y = list(D9[1])

s = np.zeros((max(y)+1, max(x)+1), dtype=np.uint8)

for i in range(len(D9)):
    s[y[i]][x[i]] = 1

for i in range(len(D9)):
    for j in range(len(D9)):
        if i != j:
            if x[i] == x[j]:
                for k in range(y[i], y[j]+1):
                    s[k][x[i]] = 1
            if y[i] == y[j]:
                for k in range(x[i], x[j]+1):
                    s[y[i]][k] = 1

plt.matshow(s)
plt.show()

#for i in range(len(s)):
#    border = []
#    for j in range(s.shape[1]):
#        if s[i][j] != 0:
#            border.append(j)
#    if len(border) >= 2:
#        for j in range(min(border), max(border) + 1):
#            if s[i][j] == 0:
#                s[i][j] = 1
