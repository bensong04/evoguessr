from ete3 import Tree
import os
import re
import random
from evo.utils import *


def randomTree(labels):
    t = Tree()
    t.populate(10, names_library=labels)
    return t

# Init Functions (return init trees)


def min_initial_species_tree(gene_trees, n):
    distances = {}
    for tree_i in gene_trees:
        distances[tree_i] = 0
        for tree_j in gene_trees:
            if tree_i != tree_j:
                distances[tree_i] += symm_duplication_cost(tree_i, tree_j)
    return min(distances, key=distances.get)


def random_from_gene_initial_species_tree(gene_trees, n):
    if n == 1:
        return random.sample(gene_trees, n)[0]
    else:
        return random.sample(gene_trees, n)


def random_true_initial_species_tree(gene_trees, n):
    return randomTree(gene_trees[0].get_leaf_names())

# Search Functions (get cost with init trees)


def greedySearch_NNI_SPR(s_t, g_t, n):
    initial_cost = sum(symm_duplication_cost(s_t, gt)
                       for gt in g_t)
    costL = [initial_cost]
    for _ in range(n):
        s_t, cost = perform_nni(s_t, g_t)
        s_t, cost = perform_spr(s_t, g_t)
        costL.append(cost)
    return costL


def greedySearch_subSwap_SPR(s_t, g_t, n):
    initial_cost = sum(symm_duplication_cost(s_t, gt)
                       for gt in g_t)
    costL = [initial_cost]
    for _ in range(n):
        s_t, cost = perform_subtreeSwap(s_t, g_t)
        s_t, cost = perform_spr(s_t, g_t)
        costL.append(cost)
    return costL


def greedySearch_NNI_only(s_t, g_t, n):
    initial_cost = sum(symm_duplication_cost(s_t, gt)
                       for gt in g_t)
    costL = [initial_cost]
    for _ in range(n):
        s_t, cost = perform_nni(s_t, g_t)
        costL.append(cost)
    return costL


def greedySearch_subSwap_only(s_t, g_t, n):
    initial_cost = sum(symm_duplication_cost(s_t, gt)
                       for gt in g_t)
    costL = [initial_cost]
    for _ in range(n):
        s_t, cost = perform_subtreeSwap(s_t, g_t)
        costL.append(cost)
    return costL


def greedySearch_SPR_only(s_t, g_t, n):
    initial_cost = sum(symm_duplication_cost(s_t, gt)
                       for gt in g_t)
    costL = [initial_cost]
    for _ in range(n):
        s_t, cost = perform_spr(s_t, g_t)
        costL.append(cost)
    return costL
# Single or Multiple Init Tree


def oneInit(initf, searchf, g_t, m):
    init_tree = initf(g_t, 1)
    costL = searchf(init_tree, g_t, m)
    return costL


def multipleInit(initf, searchf, g_t, n, m):
    init_tree_L = initf(g_t, n)
    costs = []
    for tri in init_tree_L:
        costL = searchf(tri, g_t,)
        costs.append(costL[-1])

    return min(costs)
