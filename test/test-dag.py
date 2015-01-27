####################################################################################################

from Elbrea.Algorithm.DirectedAcyclicGraph import DirectedAcyclicGraph

####################################################################################################

# http://networkx.github.io/documentation/networkx-1.9.1/

####################################################################################################

dag = DirectedAcyclicGraph()
for i in range(1, 8):
    dag.add_node(i)
for ancestor_id, descendant_id in (
        (1, 2), (2, 4), (4, 6),
        (1, 3), (3, 5), (5, 6),
        (1, 7),
):
    ancestor = dag[ancestor_id]
    descendant = dag[descendant_id]
    dag.add_edge(ancestor, descendant)

print(dag.roots())
print(dag.leafs())
print(dag.topological_sort())
print(list(dag[1].breadth_first_search()))

####################################################################################################
# 
# End
# 
####################################################################################################
