import networkx as nx
import nxmetis
from nxmetis.types import MetisOptions
import matplotlib.pyplot as plt
from random import randint
import numpy as np

def draw_graph(G, partitioning, alg_name="ex", graph_type="DGM", num=0):
    fig = plt.figure()
    colors, color_map = [], []
    n = len(partitioning)
    print("DRAW", alg_name, partitioning)
    for i in range(n):
        colors.append('#%06X' % randint(0, 0xFFFFFF))
    for i, c in zip(range(n), colors):
        for node in G:
            if alg_name != "metis":
                node = int(node)
                #print(node)
            if node in partitioning[i]:
                #print("FIND", node, i)
                color_map.append(c)
    nx.draw(G, ax=fig.add_subplot(), node_color=color_map, with_labels=True)
    fig.savefig(graph_type + "-" + str(num) + ".png")
    
G = nx.dorogovtsev_goltsev_mendes_graph(4)
print(nxmetis.partition(G, 6))
draw_graph(G, nxmetis.partition(G, 6)[1], num=0)
print(nxmetis.partition(G, 6, options = MetisOptions(contig = True)))
draw_graph(G, nxmetis.partition(G, 6, options = MetisOptions(contig = True))[1], num=1)
