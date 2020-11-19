import matplotlib.pyplot as plt
import numpy as np

from genetic_algorithm import json_editor


def plot_2d_boxplot(data):
    fig1, ax1 = plt.subplots()
    ax1.set_title('Basic Plot')
    ax1.boxplot(data)


def plot2d_data_to_axes(ax, data, size=1, alpha=0.6, color="red", interp_points=200):
    x = [int(k) for k in data.keys()]
    x.sort()
    y = [data[str(i)] for i in x]

    if (interp_points > 0):
        x_new = np.linspace(x[0], x[-1], interp_points)
        y_smooth = np.interp(x_new, x, y)
        x = x_new
        y = y_smooth

    ax.plot(x, y, linewidth=size, color=color)


def plot2d_2_series_from_path(path):
    data_read = json_editor.read_dict(path + "values")
    data = data_read["fitness"]
    data2 = data_read["novelty"]
    if len(data2.keys()) == 0:
        plot2d_2_series(data, data2, path + "values_graph", "generations", "fitness")
    else:
        plot2d_2_series(data, data2, path + "values_graph", "generations", "fitness and novelty")

    data_read2 = json_editor.read_dict(path + "ncd")
    plot2d(data_read2, path + "ncd", "generations", "ncd")
    data_read3 = json_editor.read_dict(path + "criterion_1")
    plot2d(data_read3, path + "criterion_1", "generations", "criterion 1")
    data_read4 = json_editor.read_dict(path + "criterion_2")
    plot2d(data_read4, path + "criterion_2", "generations", "criterion 2")


def plot2d_2_series(data, data2, path, x_label, y_label):
    ax = plt.axes()
    ax.set_ylim(0, 1)

    plot2d_data_to_axes(ax, data, color="red")
    plot2d_data_to_axes(ax, data2, color="blue")

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.savefig(path)
    plt.clf()
    plt.close()


def plot2d(data, path, x_label, y_label):
    ax = plt.axes()
    ax.set_ylim(0, 1)

    plot2d_data_to_axes(ax, data, color="red")

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.savefig(path)
    plt.clf()
    plt.close()


def plot2d_no_lim(data, path, x_label, y_label):
    ax = plt.axes()
    for i in data.keys():
        ax.plot([i], [data[i]], marker='o', markersize=2, alpha=0.6,
                color="red")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.savefig(path)
    plt.clf()
    plt.close()


def plot2d_data_to_axes(ax, data, size=1, alpha=0.6, color="red", interp_points=200):
    x = [int(k) for k in data.keys()]
    x.sort()
    y = [data[i] for i in x]

    if (interp_points > 0):
        x_new = np.linspace(x[0], x[-1], interp_points)
        y_smooth = np.interp(x_new, x, y)
        x = x_new
        y = y_smooth

    ax.plot(x, y, linewidth=size, color=color)


def plot2d(data, path, x_label, y_label):
    ax = plt.axes()
    ax.set_ylim(0, 1)
    for i in data.keys():
        ax.plot([i], [data[i]], marker='o', markersize=2, alpha=0.6,
                color="red")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.savefig(path)
    plt.clf()
    plt.close()


def plot2d_fit_nov(data, data2, path):
    ax = plt.axes()
    for i in data:
        print
        ax.plot([i.fitness.values[0]], [i.fitness.values[1]], marker='o', markersize=5, alpha=0.6,
                color="black")
    for i in data2:
        ax.plot([i.fitness.values[0]], [i.fitness.values[1]], marker='o', markersize=5, alpha=0.6,
                color="yellow")
    ax.set_xlabel('fitness')
    ax.set_ylabel('novelty')
    plt.axis('equal')

    plt.savefig(path + "plot.png")
    plt.clf()
    plt.close()
