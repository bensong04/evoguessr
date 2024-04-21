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
    for node in gene_tree.traverse():
        if node.is_leaf():
            continue
        leaf_labels = [leaf.name for leaf in node.iter_leaves()]
        lca_node = species_tree.get_common_ancestor(leaf_labels)
        lca_map[node] = lca_node
        parent_lca = lca_map[node.up] if node.up else None
        if parent_lca and parent_lca == lca_node:
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


def perform_nni(species_tree, gene_trees):
    best_cost = sum(symm_duplication_cost(species_tree, gt)
                    for gt in gene_trees)
    temp_tree = species_tree.copy()
    best_tree = species_tree

    # Traverse internal nodes excluding the root, and perform NNI
    for node in temp_tree.traverse("levelorder"):
        if not node.is_leaf() and not node.is_root() and len(node.children) == 2:
            # Perform the swap of children
            node.swap_children()

            # Evaluate cost after swap
            nni_cost = sum(symm_duplication_cost(temp_tree, gt)
                           for gt in gene_trees)
            if nni_cost < best_cost:
                best_cost = nni_cost
                best_tree = temp_tree.copy()

            node.swap_children()
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

            # Get ancestors to prevent invalid reattachment
            node_ancestors = node.get_ancestors()

            # Try regrafting the detached subtree at every possible point in the tree
            for potential_reattach in temp_tree.traverse("preorder"):
                if potential_reattach not in node_ancestors and potential_reattach != node:
                    # Temporarily reattach the subtree
                    potential_reattach.add_child(node)
                    # Evaluate new tree configuration
                    current_cost = sum(symm_duplication_cost(temp_tree, gt)
                                       for gt in gene_trees)
                    if current_cost < best_cost:
                        best_cost = current_cost
                        # If better, keep this configuration
                        best_tree = temp_tree.copy()

                    # Remove the subtree to try the next regraft point
                    node.detach()

            # Reattach the subtree back to its original parent if no better tree was found
            parent.add_child(node)
    return best_tree, best_cost


def main():
    gene_trees = load_gene_trees("src/trees")
    species_tree = initial_species_tree(gene_trees)
    print("Initial Species Tree:", species_tree.write(format=1))

    for _ in range(5):
        species_tree, cost = perform_nni(species_tree, gene_trees)
        species_tree, cost = perform_spr(species_tree, gene_trees)
        species_tree.show()
        print("Cost:", cost)


if __name__ == "__main__":
    main()
