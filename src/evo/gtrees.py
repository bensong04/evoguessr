"""
Library for representing and performing basic operations with gene trees.

A *gene* is a namedtuple with two fields:
- `.dna` contains the nucleotide sequence for this gene;
- `.species` is the species ID associated with this gene.
"""
from typing import NamedTuple, Self
import json

class Gene(NamedTuple):
    dna: str
    species: int

class TreeNode:
    left_child: Self
    right_child: Self
    value: Gene

class Tree:
    def __init__(self, json_str: str):
        """
        :param str json_str JSON string representing this gene tree's basic structure.
        """
        self.root: Gene = None
        self.raw: dict = json.loads(json_str)

        self._init_json()

    def _init_json(self):
        pass