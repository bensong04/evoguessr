# Heuristic notes

## Terminology

**Nearest Neighbor Exchange (NNI):** Older heuristic developed by R. Guigó, I. Muchnik, and T. Smith in 1996. See [here](NNI.pdf).

**Cut and Paste (CP):** Seems to be another older heuristic, this time developed by D. Swofford and G. Olsen. I couldn't find it online; it might be available in Sorrells?

**Leaf Labels $(L(T))$:** The set of leaf labels in a species or gene tree $T$. 

**LCA mapping $(M: T_1\rightarrow T_2)$:** A mapping from a gene tree $T_1$ to a species tree $T_2$ where $L(T_1) \subseteq L(T_2)$, such that for each $g\in T_1$, $M(g)$ represents the node in $T_2$ furthest from the root that is still an ancestor of $g$. In plain English, $M(g)$ is the most differentiated species that contains gene $g$ _(can someone verify?)_.

**Duplication/Duplication Cost $(t_{dup}(T_1, T_2))$:** The number of "duplicated" nodes under the mapping $M: T_1\rightarrow T_2$. A node $x\in T_1$ is said to be "duplicated" iff there is some child of $x$, call it $c$, such that $M(c) = M(x)$. In plain English, duplication describes when the child of a gene (in a gene tree) occurs in the same species as the parent gene _(can someone verify?)_.

**Symmetric Duplication Cost:** A measure defined on full binary trees (the set $T$ of full binary trees, equipped with $d(.,.)$, forms a metric space). Defined in the paper as 
$$\frac{t_{dup}(T_1, T_2) + t_{dup}(T_2, T_1)}{2}.$$