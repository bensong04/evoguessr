from ete3 import Tree
import os
import re


def is_internal_node(tree_node):  # only nodes whose children are also nonleaves
    return not tree_node.is_leaf()


def nni(tree: Tree):
    all_nodes = list(tree.traverse())
    nni_trees = list()
    internal_nodes = filter(is_internal_node, all_nodes)
    for A in internal_nodes:
        adj_nodes = A.get_children()
        adj_internal_nodes = [
            node for node in adj_nodes if node in internal_nodes]
        for B in adj_internal_nodes:
            A_children = list(A.get_children())
            A_children.remove(B)
            B_children = list(B.get_children())
            for a_child in A_children:
                for b_child in B_children:

                    a_child.detach()
                    b_child.detach()
                    A.add_child(b_child)
                    B.add_child(a_child)
                    tree.show()
                    nni_trees.append(tree.copy("deepcopy"))
                    a_child.detach()
                    b_child.detach()
                    A.add_child(a_child)
                    B.add_child(b_child)

    return nni_trees


def main():
    t = Tree()
    rooted = t.add_child(name="R")
    rooted.populate(10, names_library=["Gorilla_gorilla", "Felis_catus", "Sus_scrofa", "Pan_paniscus",
                    "Homo_sapiens", "Canis_lupus", "Ailuropoda_melanoleuca", "Ovis_aries", "Bos_taurus", "Gallus_gallus"])
    print("showinging initial")
    rooted.show()
    print("showing nni trees")
    nni(rooted)


main()
