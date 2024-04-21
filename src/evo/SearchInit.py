from ete3 import Tree
import os
import re
import random
from utils import *

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
    if n == 1: return random.sample(gene_trees, n)[0]
    else: return random.sample(gene_trees, n)

def random_true_initial_species_tree(gene_trees, n):
    return randomTree(gene_trees[0].get_leaf_names())

# Search Functions (get cost with init trees)
def greedySearch_NNI_SPR(s_t, g_t):
    oldcost = float('inf')
    tally = 0 #num of iterations
    costL = [] #list of cost per iteration
    while True:
        s_t, cost = perform_nni(s_t, g_t)
        s_t, cost = perform_spr(s_t, g_t)
        print("Cost:", cost)
        newcost = cost
        if newcost >= oldcost: return (costL, cost, tally)
        else:
            costL.append(newcost)
            oldcost = newcost
            tally += 1

def greedySearch_subSwap_SPR(s_t, g_t):
    oldcost = float('inf')
    tally = 0
    costL = []
    while True:
        s_t, cost = perform_subtreeSwap(s_t, g_t)
        s_t, cost = perform_spr(s_t, g_t)
        print("Cost:", cost)
        newcost = cost
        if newcost >= oldcost: return (costL, cost, tally)
        else:
            costL.append(newcost)
            oldcost = newcost
            tally += 1

def greedySearch_NNI_only(s_t, g_t):
    oldcost = float('inf')
    tally = 0
    costL = []
    while True:
        s_t, cost = perform_nni(s_t, g_t)
        print("Cost:", cost)
        newcost = cost
        if newcost >= oldcost: return (costL, cost, tally)
        else:
            costL.append(newcost)
            oldcost = newcost
            tally += 1

def greedySearch_subSwap_only(s_t, g_t):
    oldcost = float('inf')
    tally = 0
    costL = []
    while True:
        s_t, cost = perform_subtreeSwap(s_t, g_t)
        print("Cost:", cost)
        newcost = cost
        if newcost >= oldcost: return (costL, cost, tally)
        else:
            costL.append(newcost)
            oldcost = newcost
            tally += 1

def greedySearch_SPR_only(s_t, g_t):
    oldcost = float('inf')
    tally = 0
    costL = []
    while True:
        s_t, cost = perform_spr(s_t, g_t)
        print("Cost:", cost)
        newcost = cost
        if newcost >= oldcost: return (costL, cost, tally)
        else:
            costL.append(newcost)
            oldcost = newcost
            tally += 1

# Single or Multiple Init Tree
def oneInit(initf, searchf, g_t):
    init_tree = initf(g_t, 1)
    costL, cost, tally = searchf(init_tree, g_t)
    return costL, cost, tally

def multipleInit(initf, searchf, g_t, n):
    init_tree_L = initf(g_t, n)
    old_cost = float('inf')
    costs = []
    for tri in init_tree_L:
        costL, cost, tally = searchf(tri, g_t)
        costs.append(cost)
    return min(costs)
