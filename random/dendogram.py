import numpy as np
import pandas as pd

labels = ["P1","P2","P3","P4","P5","P6","P7","P8","P9","P10"]

distance_matrix = np.array([
[0,1.41,6.4,7.28,6.32,9.85,2,8.06,4.47,4.47],
[1.41,0,6.71,6.71,7.07,9.43,1.41,7.28,5.1,4.24],
[6.4,6.71,0,4.24,2.24,5.1,5.39,5.66,2.24,3],
[7.28,6.71,4.24,0,6.4,2.83,5.39,1.41,5.39,3],
[6.32,7.07,2.24,6.4,0,7.28,6,7.81,2,4.47],
[9.85,9.43,5.1,2.83,7.28,0,8.06,3.16,7,5.39],
[2,1.41,5.39,5.39,6,8.06,0,6.08,4,2.83],
[8.06,7.28,5.66,1.41,7.81,3.16,6.08,0,6.71,4.12],
[4.47,5.1,2.24,5.39,2,7,4,6.71,0,2.83],
[4.47,4.24,3,3,4.47,5.39,2.83,4.12,2.83,0]
])

clusters = [[i] for i in range(len(labels))]
cluster_names = labels.copy()

def avg_distance(c1, c2):
    d = []
    for i in c1:
        for j in c2:
            d.append(distance_matrix[i][j])
    return np.mean(d)

iteration = 1

while len(clusters) > 1:

    size = len(clusters)
    dist_matrix = np.zeros((size,size))

    for i in range(size):
        for j in range(size):
            if i != j:
                dist_matrix[i][j] = avg_distance(clusters[i], clusters[j])

    print(f"\nITERASI {iteration}")
    df = pd.DataFrame(dist_matrix, columns=cluster_names, index=cluster_names)
    print(df.round(3))

    min_val = np.inf
    pair = (0,1)

    for i in range(size):
        for j in range(i+1,size):
            if dist_matrix[i][j] < min_val:
                min_val = dist_matrix[i][j]
                pair = (i,j)

    i,j = pair

    print(f"\nMerge: {cluster_names[i]} + {cluster_names[j]}  (distance = {min_val:.2f})")

    new_cluster = clusters[i] + clusters[j]
    new_name = f"({cluster_names[i]},{cluster_names[j]})"

    clusters.append(new_cluster)
    cluster_names.append(new_name)

    for idx in sorted([i,j], reverse=True):
        del clusters[idx]
        del cluster_names[idx]

    iteration += 1

    if(iteration > 10):
        break