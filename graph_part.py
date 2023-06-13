import networkx as nx
import matplotlib.pyplot as plt
import nxmetis
from random import randint


def draw_graph(partitioning, alg_name, graph_type):
    fig = plt.figure()
    colors, color_map = [], []
    n = len(partitioning)
    for i in range(n):
        color = '#%06X' % randint(0, 0xFFFFFF)
        for node in G:
            if node in partitioning[i]:
                color_map.append(color)
    nx.draw(G, ax=fig.add_subplot(), node_color=color_map, with_labels=True)
    fig.savefig("graph-" + alg_name + "-" +  graph_type + ".png")

G = nx.complete_graph(10)
partitioning = nxmetis.partition(G, 2)[1]
print(partitioning)
draw_graph(partitioning, "metis", "complete")
