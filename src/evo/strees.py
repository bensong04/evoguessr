"""
Species trees
"""
from typing import NamedTuple, Self, Optional, Any
from collections import deque
from dataclasses import dataclass
from .trees import TreeNode, Tree

@dataclass
class SpeciesNode:
    left_child: Optional[Self]
    right_child: Optional[Self]
    value: Optional[int]

class SpeciesTree(Tree[SpeciesNode]):
    def __init__(self):
        super().__init__()
    