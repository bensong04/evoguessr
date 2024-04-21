from ete3 import Tree
import os
import re


def is_internal_node (tree_node):
    return not tree_node.is_leaf()

def nni (tree : Tree):
    all_nodes = list(tree.traverse())
    return None
def main():
    t = Tree()
    rooted = t.add_child(name="R")
    rooted.populate(10, names_library=list("abcdefghij"))
    nni (rooted)

    rooted.show()
    
main()