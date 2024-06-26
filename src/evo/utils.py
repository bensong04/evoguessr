from ete3 import Tree
import os
import re


def extract_species(label):
    match = re.search(r'OS=([^_]+_[^_]+)', label)
    if match:
        return match.group(1)
    else:
        return None


def preprocess_newick_file(file_path):
    # Read the entire content of the file
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Process each line
    processed_lines = []
    for line in lines:
        line = line.strip()
        parts = re.split(r'(\(|\)|,)', line)
        new_parts = []
        for part in parts:
            species = extract_species(part)
            if species:
                new_parts.append(species)
            else:
                new_parts.append(part)
        # Join all parts to reform the Newick string
        processed_line = ''.join(new_parts)
        processed_lines.append(processed_line)

    # Write the processed content back to the same file
    with open(file_path, 'w') as f:
        for line in processed_lines:
            f.write(line + '\n')


def load_gene_trees(path):
    tree_list = []
    for filename in os.listdir(path):
        if filename.endswith('.nwk'):
            file_path = os.path.join(path, filename)
            preprocess_newick_file(file_path)
            tree = Tree(file_path, format=1)
            tree_list.append(tree)
    return tree_list


def duplication_cost(species_tree, gene_tree):
    lca_map = {}
    duplication_cost = 0
    leaf_names = species_tree.get_leaf_names()
    try:
        for node in gene_tree.traverse():
            if node.is_leaf():
                lca_map[node] = species_tree.search_nodes(
                    name=node.name)[0]
                continue

            leaves = node.get_leaves()
            leaf_labels = []

            for leaf in leaves:
                name = leaf.name
                if name not in leaf_names:
                    continue
                leaf_labels.append(species_tree.get_leaves_by_name(name)[0])
            if len(leaf_labels) < 2:
                continue
            lca_node = species_tree.get_common_ancestor(leaf_labels)
            lca_map[node] = lca_node

    except Exception as e:
        print(leaves)
        species_tree.show()
        raise e

    for node in gene_tree.traverse():
        if node not in lca_map or node.is_leaf():
            continue
        for child in node.children:
            if child not in lca_map:
                continue
            if lca_map[child] == lca_map[node]:
                duplication_cost += 1
    return duplication_cost


def symm_duplication_cost(t1, t2):
    return (duplication_cost(t1, t2) + duplication_cost(t2, t1)) / 2


def initial_species_tree(gene_trees):
    distances = {}
    for tree_i in gene_trees:
        distances[tree_i] = 0
        for tree_j in gene_trees:
            if tree_i != tree_j:
                distances[tree_i] += symm_duplication_cost(tree_i, tree_j)
    return min(distances, key=distances.get)


def perform_subtreeSwap(species_tree, gene_trees):
    best_cost = sum(symm_duplication_cost(species_tree, gt)
                    for gt in gene_trees)
    temp_tree = species_tree.copy()
    best_tree = species_tree

    # Traverse internal nodes excluding the root, and perform NNI
    for nodei in temp_tree.traverse("levelorder"):
        if not nodei.is_leaf() and not nodei.is_root() and len(nodei.children) == 2:
            for nodej in temp_tree.traverse("levelorder"):
                if not nodej.is_leaf() and not nodej.is_root() and len(nodej.children) == 2 and nodej != nodei:
                    nodei_ancestors = nodei.get_ancestors()
                    nodej_ancestors = nodej.get_ancestors()

                    if nodei in nodej_ancestors or nodej in nodei_ancestors:
                        continue

                    # Perform the swap of children
                    c1 = nodei.children[0]
                    c2 = nodej.children[0]

                    c1.detach()
                    c2.detach()
                    nodei.add_child(c2)
                    nodej.add_child(c1)

                    # Evaluate cost after swap
                    cost = sum(symm_duplication_cost(temp_tree, gt)
                               for gt in gene_trees)
                    if cost < best_cost:
                        best_cost = cost
                        best_tree = temp_tree.copy()
                        return best_tree, best_cost
                    # undo
                    c1 = nodei.children[1]
                    c2 = nodej.children[1]
                    c1.detach()
                    c2.detach()
                    nodei.add_child(c2)
                    nodej.add_child(c1)

    return best_tree, best_cost


def is_internal_node(tree_node):  # only nodes whose children are also nonleaves
    return not tree_node.is_leaf()


def perform_nni(species_tree, gene_trees):
    best_cost = sum(symm_duplication_cost(species_tree, gt)
                    for gt in gene_trees)
    best_tree = species_tree

    all_nodes = list(species_tree.traverse())
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
                    nni_trees.append(species_tree.copy("deepcopy"))
                    a_child.detach()
                    b_child.detach()
                    A.add_child(a_child)
                    B.add_child(b_child)

    for tree in nni_trees:
        cost = sum(symm_duplication_cost(tree, gt)
                   for gt in gene_trees)
        if cost < best_cost:
            best_cost = cost
            best_tree = tree
            return best_tree, best_cost

    return best_tree, best_cost


def perform_spr(species_tree, gene_trees):
    best_cost = sum(symm_duplication_cost(species_tree, gt)
                    for gt in gene_trees)
    temp_tree = species_tree.copy()
    best_tree = species_tree
    # Iterate over all possible nodes to prune
    for node in temp_tree.traverse("postorder"):
        if not node.is_root() and not node.is_leaf():
            parent = node.up  # Save the parent node for reattachment
            node.detach()  # Detach the node

            # Try regrafting the detached subtree at every possible point in the tree
            for potential_reattach in temp_tree.traverse("preorder"):
                if potential_reattach != node and not potential_reattach.is_leaf():
                    # Temporarily reattach the subtree
                    potential_reattach.add_child(node)
                    # Evaluate new tree configuration
                    current_cost = sum(symm_duplication_cost(temp_tree, gt)
                                       for gt in gene_trees)
                    if current_cost < best_cost:
                        best_cost = current_cost
                        best_tree = temp_tree.copy()
                        return best_tree, best_cost

                    # Remove the subtree to try the next regraft point
                    node.detach()

            # Reattach the subtree back to its original parent if no better tree was found
            parent.add_child(node)
    return best_tree, best_cost


def randomTree(labels):
    t = Tree()
    t.populate(10, names_library=labels)
    return t


def main():
    gene_trees = load_gene_trees("src/trees")
    species_tree = initial_species_tree(gene_trees)
    species_tree = randomTree(species_tree.get_leaf_names())
    initial_cost = sum(symm_duplication_cost(species_tree, gt)
                       for gt in gene_trees)
    print("initial cost", initial_cost)
    species_tree.show()
    for _ in range(10):
        # species_tree, cost = perform_subtreeSwap(species_tree, gene_trees)
        species_tree, cost = perform_spr(species_tree, gene_trees)
        print("Cost:", cost)


if __name__ == "__main__":
    main()
