"""
Library for representing and performing basic operations with gene trees.

A *gene* is a namedtuple with two fields:
- `.dna` contains the nucleotide sequence for this gene;
- `.species` is the species ID associated with this gene.

The associated species for a *contemporary* gene should be the species 
containing that gene, while for an *ancestral* gene, it should be the
most recent species containing that gene -- this is the LCA mapping.

Since gene trees also contain the LCA mapping, we can easily compute
t_dup between a gene tree and a species tree.
"""
from typing import NamedTuple, Self, Optional, Any, TypeAlias
from collections import deque
from dataclasses import dataclass
from .trees import TreeNode, Tree

import json

class Gene(NamedTuple):
    dna: str
    species: int

type GeneNode = TreeNode[Gene]

class GeneTree(Tree[GeneNode]):
    def __init__(self, json_str: str):
        """
        :param str json_str JSON string representing this gene tree's basic structure.
        """
        super().__init__()
        self.raw: dict = json.loads(json_str)
        # Initialize tree
        self._init_json()

    def _init_json(self):
        # dfs
        def _dfs(node_to_fill: GeneNode, label: str, entry_in_json: Any):
            # fill in node with content
            val = label
            species_val, dna_val = val.split(',', 2)
            # assume structure of input JSON file
            node_to_fill.value = Gene(dna=dna_val, species=species_val)
            if len(entry_in_json) == 0:
                # nothing to be done
                return
            elif len(entry_in_json) >= 1:
                # recurse on left child
                node_to_fill.left_child = TreeNode(None, None, None)
                left = list(entry_in_json)[0]
                _dfs(node_to_fill.left_child, left, entry_in_json[left])
            if len(entry_in_json) == 2:
                # then fill in the right child as well
                node_to_fill.right_child = TreeNode(None, None, None)
                right = list(entry_in_json)[1]
                _dfs(node_to_fill.right_child, right, entry_in_json[right])
        root_label = next(iter(self.raw))
        _dfs(self.root, root_label, self.raw[root_label])