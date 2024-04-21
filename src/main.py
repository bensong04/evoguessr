from ete3 import Tree
import os
import re
from evo.utils import load_gene_trees, initial_species_tree, randomTree, perform_nni, perform_spr

def main():
    gene_trees = load_gene_trees("./trees")
    species_tree = initial_species_tree(gene_trees)
    species_tree = randomTree(species_tree.get_leaf_names())
    for _ in range(5):
        species_tree, cost = perform_nni(species_tree, gene_trees)
        species_tree, cost = perform_spr(species_tree, gene_trees)
        print("Cost:", cost)


if __name__ == "__main__":
    main()