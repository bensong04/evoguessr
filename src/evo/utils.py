"""
Defines various useful operations on gene/species trees.
"""
import dendropy
import os
import re
import copy


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
    """Load gene trees from a file."""

    tree_list = dendropy.TreeList()
    for filename in os.listdir(path):
        if filename.endswith('.nwk'):  # Assuming tree files have ".tre" extension
            file_path = os.path.join(path, filename)

            preprocess_newick_file(file_path)

            trees = dendropy.TreeList.get_from_path(
                file_path, schema='newick')
            tree_list.extend(trees)

    return tree_list


def duplication_cost(species_tree, gene_tree):
    """Map each node in gene tree to the LCA in the species tree, return duplication cost."""
    lca_map = {}
    duplication_cost = 0
    for node in gene_tree:
        if node.is_leaf():
            continue
        leaf_labels = [leaf.taxon.label for leaf in node.leaf_iter()]
        lca_taxa = species_tree.mrca(taxon_labels=leaf_labels)
        lca_map[node] = lca_taxa
        parent_lca = lca_map[node.parent_node] if node.parent_node else None
        if parent_lca and parent_lca == lca_taxa:
            duplication_cost += 1
    return duplication_cost


def symm_duplication_cost(t1, t2):
    return (duplication_cost(t1, t2) + duplication_cost(t2, t1))/2


def initial_species_tree(gene_trees):
    distances = {}
    for i in range(len(gene_trees)):
        tree_i = gene_trees[i]
        distances[tree_i] = 0
        for j in range(len(gene_trees)):
            if i != j:
                tree_j = gene_trees[j]
                distances[tree_i] += symm_duplication_cost(tree_i, tree_j)

    # Find the tree with the minimal total symmetric dup difference
    initial_species_tree = min(distances, key=distances.get)
    return initial_species_tree


def apply_nni(species_tree, gene_trees):
    """Apply NNI to minimize the duplication cost."""
    best_cost = sum(symm_duplication_cost(species_tree, gt)
                    for gt in gene_trees)
    best_tree = species_tree.clone()
    count = 0
    for edge in species_tree.internal_edges():
        if not edge.is_terminal() and edge.head_node and edge.tail_node:
            species_tree.reroot_at_edge(edge, update_bipartitions=True)
            nni_cost = sum(duplication_cost(species_tree, gt)
                           for gt in gene_trees)
            count += 1
            if nni_cost < best_cost:
                best_cost = nni_cost
                best_tree = species_tree.clone()
            species_tree.reroot_at_edge(
                edge, update_bipartitions=True)  # undo NNI
    print(count)
    return best_tree, best_cost


def perform_spr(species_tree, gene_trees):
    """Apply Subtree Pruning and Regrafting (SPR) to improve the species tree."""
    best_cost = sum(symm_duplication_cost(species_tree, gt)
                    for gt in gene_trees)
    best_tree = dendropy.Tree(species_tree)
    count = 0
    tempTree = dendropy.Tree(species_tree)
    # Function to check if a node is the root or directly connected to the root

    def is_connected_to_root(node, tree):
        return node is tree.seed_node or node.parent_node is tree.seed_node

    for prune_node in tempTree.nodes():
        if prune_node.is_internal() and not is_connected_to_root(prune_node, tempTree):
            parent_node = prune_node.parent_node
            siblings = parent_node.child_nodes()
            siblings.remove(prune_node)

            # Temporarily remove the prune_node to test regraft locations
            parent_node.remove_child(prune_node)

            for regraft_node in tempTree.postorder_node_iter():
                if regraft_node not in prune_node.ancestor_iter():
                    regraft_node.add_child(prune_node)
                    count += 1
                    print(count, tempTree.as_string(schema="newick"))
                    current_cost = sum(symm_duplication_cost(
                        tempTree, gt) for gt in gene_trees)
                    if current_cost < best_cost:
                        best_cost = current_cost
                        # Only create a new tree if it's actually better
                        best_tree = dendropy.Tree(tempTree)
                    # Revert changes to regraft location for next iteration
                    regraft_node.remove_child(prune_node)

            # Restore original parent connection after testing all regraft locations
            parent_node.add_child(prune_node)

    print("Total regraft attempts:", count)
    return best_tree, best_cost


def main():
    gene_trees = load_gene_trees("src/trees")  # add path here
    species_tree = initial_species_tree(gene_trees)
    print("Initial Species Tree:", species_tree.as_string(schema="newick"))

    for _ in range(10):  # Iterate to refine the tree
        species_tree, cost = apply_nni(species_tree, gene_trees)
        species_tree, cost = perform_spr(species_tree, gene_trees)

        print("Refined Species Tree:", species_tree.as_string(
            schema="newick"), "Cost:", cost)


if __name__ == "__main__":
    main()

"""
# SPR code using builtin method
for i in range(num_iterations):
	# Make a copy of the current tree
	tree_copy = best_tree.clone()

	# Perform a random SPR operation on the copy
	tree_copy.spr_prune_regraft_random()

	# Calculate the metric for the new tree
	new_metric = metric(tree_copy)

	# If the new tree is better, update the best tree and metric
	if new_metric < best_metric:
		best_tree = tree_copy
		best_metric = new_metric
"""

"""
# NNI code using builtin method
for i in range(num_iterations):
	# Make a copy of the current tree
	tree_copy = best_tree.clone()

	# Perform a random NNI operation on the copy
	tree_copy.nniswap_random()

	# Calculate the metric for the new tree
	new_metric = metric(tree_copy)

	# If the new tree is better, update the best tree and metric
	if new_metric < best_metric:
		best_tree = tree_copy
		best_metric = new_metri
"""

"""
Search Paradigm Variations
1. keep best n results as starting tree (total symmetric cost) instead of 1
2. ALternate NNI, SPR, iterate when we see improvement
4. Do NNI only
5. Do SPR only
6. The Kashtan-Alon Algorithm as higher architecture
7. Incorporate randomness to allow for exploration
"""