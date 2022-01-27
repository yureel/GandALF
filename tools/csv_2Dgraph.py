import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


def csv_2d_graph_effect(csv_file, i, j, x_name, y_name):
    font = FontProperties(family='Arial',
                          weight='normal',
                          style='normal', size=16)
    plt.rc('font', size=16)
    x = pd.read_csv(csv_file + '.csv')
    a = x.values
    inputs = a[:, i]
    outputs = a[:, j]
    print(inputs, outputs)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    for k in range(len(inputs)):
        if a[k, 0] == 1:
            plt.scatter(inputs[k], outputs[k], c='blue')
        elif a[k, 1] == 1:
            plt.scatter(inputs[k], outputs[k], c='green')
        elif a[k, 2] == 1:
            plt.scatter(inputs[k], outputs[k], c='orange')
    plt.savefig(csv_file + '.png', bbox_inches = 'tight')
    plt.show()


def csv_2d_graph_TH(csv_file, i, j, x_name, y_name):
    font = FontProperties(family='Arial',
                          weight='normal',
                          style='normal', size=16)
    plt.rc('font', size=16)
    x = pd.read_csv(csv_file + '.csv')
    a = x.values
    inputs = a[:, i]
    outputs = a[:, j]
    print(inputs, outputs)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    for k in range(len(inputs)):
        if k < 50:
            plt.scatter(inputs[k], outputs[k], c='orange')
        else:
            plt.scatter(inputs[k], outputs[k], c='blue')
    plt.savefig(csv_file + '.png', bbox_inches='tight')
    plt.show()


def csv_2d_graph_learning(csv_file, i, L, x_name, y_name, d, e, name_file, labels=None):
    font = FontProperties(family='Arial',
                          weight='normal',
                          style='normal', size=16)
    plt.rc('font', size=16)
    x = pd.read_csv(csv_file + '.csv')
    a = x.values
    ax = plt.subplot(111)
    ax.set_xlim(d, e)
    marker = ['.', 'v', '.', '.', '.', '^', '.', '.']
    inputs = a[:, i]
    for j in L:
        print(j)
        outputs = a[:, j]
        print(inputs, outputs)
        if j == 3:
            plt.plot(inputs, outputs, marker=marker[j-1], markersize='10', label=labels[j-1], color='grey')
        else:
            plt.plot(inputs, outputs, marker=marker[j-1], markersize='7', label=labels[j-1])
    plt.plot(inputs, a[:, 7], marker='s', markersize='5', label='Random', color='green')
    plt.fill_between(inputs, a[:, 7]+2*a[:, 9], a[:, 7]-2*a[:, 9], color='green', alpha=0.2, label='95% CI')
    plt.legend(loc=0)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.savefig(name_file + '.png', bbox_inches='tight')
    plt.show()
