import dendropy


def perform_nni(tree):
    # Iterate over internal nodes to find a suitable candidate for NNI
    for node in tree.postorder_node_iter():
        if node.is_internal() and not node.is_leaf() and node.parent_node is not None:
            children = node.child_nodes()
            if len(children) == 2 and children[0].is_internal() and children[1].is_internal():
                # We select grandchildren from both children
                grandchild1 = children[0].child_nodes()[0]
                grandchild2 = children[1].child_nodes()[0]

                # Swap grandchildren between the two children
                children[0].remove_child(grandchild1)
                children[1].remove_child(grandchild2)

                children[0].add_child(grandchild2)
                children[1].add_child(grandchild1)

                # Break after first successful NNI to avoid multiple swaps in one execution
                break


# Sample tree in Newick format
newick_str = "((A,(B,C)),(D,E));"
tree = dendropy.Tree.get(
    data=newick_str, schema="newick", rooting='force-rooted')

print("Original tree:")
print(tree.as_string(schema="newick"))

# Perform NNI on the provided tree
perform_nni(tree)

print("Tree after NNI:")
print(tree.as_string(schema="newick"))
