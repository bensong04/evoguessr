"""
Defines various useful operations on gene/species trees.
"""
from .gtrees import GeneNode, GeneTree
from .strees import SpeciesNode, SpeciesTree

def t_dup(g: GeneTree, s: SpeciesTree):
    """
    Calculates t_dup(G, S) as defined in the original paper.
    """
    pass