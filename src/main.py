import dendropy
import os
import re


def extract_species(label):
    # Updated to capture two words joined by an underscore
    match = re.search(r'OS=([^_]+)', label)
    if match:
        return match.group(1)
    else:
        return None


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
    species_tree.encode_bipartitions()
    gene_tree.encode_bipartitions()
    lca_map = {}
    duplication_cost = 0
    for node in gene_tree:
        if node.is_leaf():
            continue
        leaf_labels = [leaf.taxon.label for leaf in node.leaf_iter()]
        print(leaf_labels)
        lca_taxa = species_tree.mrca(taxon_labels=leaf_labels)
        lca_map[node] = lca_taxa
        parent_lca = lca_map[node.parent_node] if node.parent_node else None
        if parent_lca and parent_lca == lca_taxa:
            duplication_cost += 1
    return duplication_cost


treeList = load_gene_trees("src/trees")
