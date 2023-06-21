import networkx as nx
import matplotlib.pyplot as plt
import nxmetis
from nxmetis.types import MetisOptions
from random import randint
import numpy as np
import pymetis

def draw_graph(G, partitioning, alg_name, graph_type, num):
    fig = plt.figure()
    colors, color_map = [], []
    n = len(partitioning)
    for i in range(n):
        colors.append('#%06X' % randint(0, 0xFFFFFF))
    for node in G:
        for i in range(n):
            if node in partitioning[i]:
                color_map.append(colors[i])
    nx.draw(G, ax=fig.add_subplot(), node_color=color_map, with_labels=True)
    fig.savefig("graphs/" + alg_name + "-" +  graph_type + "-obj_func" + str(num) + ".png")

def cut(G, groups, first_group, second_group):
    cut_size = 0
    for edge in G.edges:
        if (edge[0] in groups[first_group] and edge[1] in groups[second_group]) or (edge[1] in groups[first_group] and edge[0] in groups[second_group]):
            cut_size += 1
    return cut_size

def vol(G, groups, group_num):
    degree = 0
    for i in groups[group_num]:
        degree += G.degree(int(i))
    return degree

def min_cut(G, groups):
    cut_size = 0
    for edge in G.edges:
        #print("EDGE", edge, edge[0], edge[1])
        for group_num in range(len(groups)):
            #print("GROUP", group_num)
            if edge[0] in groups[group_num] and edge[1] not in groups[group_num]:
                cut_size += 1
    return cut_size

def ratio_cut(G, groups):
    res = 0
    for i in range(len(groups)):
        for j in range(i, len(groups)):
            if i != j:
                #print(cut(G, groups, i, j)/len(groups[i]), cut(G, groups, i, j)/len(groups[j]))
                res += cut(G, groups, i, j)/len(groups[i]) + cut(G, groups, i, j)/len(groups[j])
    return res

def normilized_cut(G, groups):
    res = 0
    for i in range(len(groups)):
        for j in range(i, len(groups)):
            if i != j:
                #print(cut(G, groups, i, j)/vol(G, groups, i) + cut(G, groups, i, j)/vol(G, groups, j))
                res += cut(G, groups, i, j)/vol(G, groups, i) + cut(G, groups, i, j)/vol(G, groups, j)
    return res

def quotient_cut(G, groups):
    res = 0
    for i in range(len(groups)):
        for j in range(i, len(groups)):
            if i != j:
                #print(cut(G, groups, i, j)/min(vol(G, groups, i), vol(G, groups, j)), vol(G, groups, i), vol(G, groups, j))
                res += cut(G, groups, i, j)/min(vol(G, groups, i), vol(G, groups, j))
    return res

def generate_subgraphs(topology, num_of_subgraphs):
        #print("SUBGRAPHS", nodes)
        return nxmetis.partition(topology, num_of_subgraphs, options = MetisOptions(ccorder = True))[1]

def swap(G, groups):
    i, j = randint(0, len(groups)-1), randint(0, len(groups)-1)
    if i == j:
        j = (i + 1) % len(groups)
    i_a, j_b = randint(0, len(groups[i])-1), randint(0, len(groups[j])-1)
    temp = groups[i][i_a]
    groups[i][i_a] = groups[j][j_b]
    groups[j][j_b] = temp
    return groups

def get_partition(G, subgraphs_num, objective):
    prev, iters = 0, 0
    best_groups = []
    groups = generate_subgraphs(G, subgraphs_num)
    while iters < 200:
        #print("groups", groups, objective)
        if objective == 0:
            obj_func = min_cut(G, groups)
        if objective == 1:
            obj_func =  ratio_cut(G, groups)
        if objective == 2:
            obj_func =  normilized_cut(G, groups)
        if objective == 3:
            obj_func = quotient_cut(G, groups)
        if iters == 0:
            prev = obj_func
            best_groups = groups
        if obj_func >= prev:
            if iters > 20:
                return best_groups
        else:
            best_groups = groups
        groups = swap(G, groups)
        iters += 1
        prev  = obj_func
    return groups

G = nx.complete_graph(24)
G1 = nx.petersen_graph()
G2 = nx.dorogovtsev_goltsev_mendes_graph(4)
G3 = nx.balanced_tree(2, 4)
num = 2
partitioning = generate_subgraphs(G1, num)
draw_graph(G1, partitioning, "metis", "petersen", num)
for i in range(4):
    partitioning = get_partition(G1, num, i)
    #print("part", i, partitioning)
    draw_graph(G1, partitioning, "obj_func_" + str(i), "petersen", num)

for num in [2, 4, 6, 8]:
    partitioning = generate_subgraphs(G, num)
    #print(num, partitioning)
    draw_graph(G, partitioning, "metis", "complete", num)
    partitioning = generate_subgraphs(G2, num)
    draw_graph(G2, partitioning, "metis", "DGM", num)
    partitioning = generate_subgraphs(G3, num)
    draw_graph(G3, partitioning, "metis", "balanced_tree", num)
    for i in range(4):
        partitioning = get_partition(G, num, i)
        #print("part", i, partitioning)
        draw_graph(G, partitioning, "obj_func_" + str(i), "complete", num)
        partitioning = get_partition(G2, num, i)
        draw_graph(G2, partitioning, "obj_func_" + str(i), "DGM", num)
        partitioning = get_partition(G3, num, i)
        draw_graph(G3, partitioning, "obj_func_" + str(i), "balanced_tree", num)
