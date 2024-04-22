from ete3 import Tree
import os
import re
from evo.utils import load_gene_trees
from evo.SearchInit import *


def main():
    gene_trees = load_gene_trees("src/trees")

    # print(oneInit(random_true_initial_species_tree,
    #             greedySearch_subSwap_SPR, gene_trees, 10))
    print(multipleInit(random_true_initial_species_tree,
          greedySearch_subSwap_SPR, gene_trees, 5, 10))


if __name__ == "__main__":
    main()
