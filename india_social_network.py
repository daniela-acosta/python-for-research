#cd C:\Users\Daniela\Desktop\Using_Python_for_Research\Case_Studies\6Social_Network_Analysis
import numpy as np
import networkx as nx

A1 = np.loadtxt("adj_allVillageRelationships_vilno_1.csv", delimiter=",")
A2 = np.loadtxt("adj_allVillageRelationships_vilno_2.csv", delimiter=",")

#Converting Adjacency matrices to graphs
G1 = nx.to_networkx_graph(A1)
G2 = nx.to_networkx_graph(A2)

def basic_net_stats(G):
    print("Number of nodes: %d" % G.number_of_nodes())
    print("Number of edges: %d" % G.number_of_edges())
    print("Average degree: %.2f" % np.mean(list(G.degree().values())))

plot_degree_distribution(G1) #Función definida en el otro archivo
plot_degree_distribution(G2)
plt.savefig("village_hist.pdf")

#Finding the Largest Connnected Component
gen = nx.connected_component_subgraphs(G1)
g = gen.__next__() 
len(gen.__next__()) #Esto nos da el tamaño de cada componente al correrlo consecutivamente, pero es muy tedioso
#si es que queremos encontrar el máximo porque el orden del tamaño de componentes es arbitrario

#Otra opción:
G1_LCC = max(nx.connected_component_subgraphs(G1), key=len)
G2_LCC = max(nx.connected_component_subgraphs(G2), key=len)

#Analizando el resultado
G1_LCC.number_of_nodes()/G1.number_of_nodes()
G2_LCC.number_of_nodes()/G2.number_of_nodes()

#Visualizing largest components in both villages
plt.figure()
nx.draw(G1_LCC, node_color="red", edge_color="gray", node_size=20)
plt.savefig("village1.pdf")

plt.figure()
nx.draw(G2_LCC, node_color="green", edge_color="gray", node_size=20)
plt.savefig("village2.pdf")