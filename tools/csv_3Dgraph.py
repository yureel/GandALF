import pandas as pd
from matplotlib import pyplot as plt


def plot_3d_graph(csv_file):
    x = pd.read_csv(csv_file)
    A = x.values
    T = A[:, 0]
    H = A[:, 1]
    Y = A[:, 2]
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(T, H, Y)
    ax.set_xlabel('T')
    ax.set_ylabel('Hprot')
    ax.set_zlabel('Crash')
    plt.show()
    print(A)
