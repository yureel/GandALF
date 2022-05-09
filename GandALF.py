from sklearn.cluster import KMeans
import GPyOpt
from Clustering import initialization_cluster, select_clusters, largest_empty_cluster, elements_cluster, select_random
from Clustering import select_uncertainty, select_EMOC, select_center, normalizer, denormalizer, rescale, descale
import numpy as np
import pandas as pd

pool_size = 100000
n_init = 10
mode = 'EMOC'  # 'uncertainty', 'EMOC' or 'center'
normalize = True  # normalize all input dimensions before clustering overwrites scale
scale = False  # scale the dimensions by an importance parameter
objective = None  # function which receives a 2 dimensional np.array as argument and returns a float

csv_file = pd.read_csv('GandALF.csv', header=None)
csv_values = csv_file.values
try:
    if csv_values[0, -1] == 'output' or csv_values[0, -1] == 'Output':
        n_variables = csv_values[0].size-2
    else:
        n_variables = csv_values[0].size - 1
except IndexError:
    n_variables = csv_values[0].size-1
lengthscale = np.ones((1, n_variables))

spacelist = []
for i in range(n_variables):
    spacelist.append({'name': csv_values[0][i+1], 'type': csv_values[3][i+1],
                      'domain': (float(csv_values[1][i+1]), float(csv_values[2][i+1]))})


space = GPyOpt.Design_space(space=spacelist)
min_values = np.array(csv_values[1, 1:1+n_variables], dtype=float)
max_values = np.array(csv_values[2, 1:1+n_variables], dtype=float)

# The initial experiments
if csv_values.shape[0] == 4:
    X, Y = initialization_cluster(space, pool_size, n_init, min_values, max_values,
                                  objective=objective, normalize=True, scale=False)
    column_1 = np.empty((n_init, 1))
    for i in range(n_init):
        column_1[i] = i+1
    if objective is not None:
        X = np.hstack((column_1, X, Y))
    else:
        X = np.hstack((column_1, X))
    with open('GandALF.csv', "ab") as f:
        np.savetxt(f, X, delimiter=',')

else:
    X = np.array(csv_values[4:, 1: -1], dtype=float)
    Y = np.array(csv_values[4:, -1], dtype=float).reshape(-1, 1)
    if np.isnan(Y[-1]):
        raise SyntaxError("The output of the last experiment is not supplied")
    pool = np.vstack((GPyOpt.experiment_design.initial_design('random', space, max(10**5, 100 * X.shape[0])), X))
    if normalize:
        pool = normalizer(pool, min_values, max_values)
    elif scale:
        pool = rescale(pool, lengthscale, min_values, max_values)
    query_cluster = 0
    while query_cluster == 0:
        cluster = KMeans(n_clusters=X.shape[0] + 1).fit(pool)
        print(cluster)
        new_cluster = select_clusters(cluster, X.shape[0])
        print(new_cluster)
        query_cluster = largest_empty_cluster(new_cluster)
        print(query_cluster)
    X_cluster = elements_cluster(cluster, query_cluster, pool)
    if normalize:
        X_cluster = denormalizer(X_cluster, min_values, max_values)
    elif scale:
        X_cluster = descale(X_cluster, lengthscale)
    if mode == 'uncertainty':
        X_new = select_uncertainty(X_cluster, X, Y, min_values, max_values)
    elif mode == 'EMOC':
        X_new, lengthscale = select_EMOC(X_cluster, X, Y, min_values, max_values)
    elif mode == 'center':
        X_new = select_center(X_cluster, cluster, query_cluster)
    elif mode == 'random':
        X_new = select_random(X_cluster)

    X = np.vstack((X, X_new))
    if objective is not None:
        Y_new = objective(np.array([X_new]))
        Y = np.vstack((Y, Y_new))
        X_new = np.hstack((np.array(X.shape[0]), X_new, Y_new))
    else:
        X_new = np.hstack((np.array(X.shape[0]), X_new))
    with open('GandALF.csv', "ab") as f:
        np.savetxt(f, X_new.reshape(1, -1), delimiter=',')
