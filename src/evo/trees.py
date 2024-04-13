"""
Generic tree library
"""
from typing import NamedTuple, Self, Optional, Any
from dataclasses import dataclass
from collections import deque

@dataclass
class TreeNode[T]:
    left_child: Optional[Self]
    right_child: Optional[Self]
    value: Optional[T]

class Tree[T]: # Maybe not the best OOP-design, but whatever
    def __init__(self):
        self.root: T = TreeNode[T]
    
    def __repr__(self):
        repres = ""
        queue = deque()
        queue.append((0, self.root))
        while queue:
            lvl, node = queue.popleft()
            if node is not None:
                repres += str(lvl) + " " + str(node.value) + "\n"
                queue.append((lvl+1, node.left_child))
                queue.append((lvl+1, node.right_child))
        return repres

    def nni(self):
        """
        Not really sure how NNI can be done on a rooted tree.
        Are all of the trees we're working with unrooted?
        Doesn't seem like it to me, just based on the diagrams.
        """
        # TODO: implement NNI.
        pass

    def subtree_reprune_graft(self):
        """
        rSPR is applied to rooted trees*, and goes: break any edge except the 
        edge leading to the root node. Join one end of the edge 
        (specifically: the end of the edge that is FURTHEST from the root) and 
        attach it to any other edge of the tree. (Wikipedia)
        """
        # TODO: implement subtree repruning and grafting
        pass