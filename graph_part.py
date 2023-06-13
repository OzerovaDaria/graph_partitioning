import networkx as nx
import matplotlib.pyplot as plt
import nxmetis
from random import randint


def draw_graph(partitioning, alg_name, graph_type, num):
    fig = plt.figure()
    colors, color_map = [], []
    n = len(partitioning)
    for i in range(n):
        colors.append('#%06X' % randint(0, 0xFFFFFF))
    for i, c in zip(range(n), colors):
        for node in G:
            if node in partitioning[i]:
                color_map.append(c)
    nx.draw(G, ax=fig.add_subplot(), node_color=color_map, with_labels=True)
    fig.savefig("graph-" + alg_name + "-" +  graph_type + "-" + str(num) + ".png")

G = nx.complete_graph(100)
for num in [2, 4, 10, 20, 25]:
    partitioning = nxmetis.partition(G, 2)[1]
    print(num, partitioning)
    draw_graph(partitioning, "metis", "complete", num)
