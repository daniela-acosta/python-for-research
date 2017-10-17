#cd C:\Users\Daniela\Desktop\Using_Python_for_Research\Case_Studies\6Social_Network_Analysis

import networkx as nx
import matplotlib.pyplot as plt

G = nx.karate_club_graph()
nx.draw(G, with_labels=True,  node_color="lightblue", edge_color="gray")
plt.savefig("karate_graph.pdf")

#4.3.3. Random Graphs
from scipy.stats import bernoulli
#Creamos un ejemplo de graph ER
def er_graph(N, p):
    """Generate an ER graph"""
    G = nx.Graph()
    G.add_nodes_from(range(N))
    for node1 in G.nodes():
        for node2 in G.nodes():
            if node1 < node2 and bernoulli.rvs(p=p): #n1<n2 para evitar repetir pares de nodos
                G.add_edge(node1, node2)
    return G

nx.draw(er_graph(50, 0.08), node_size=40, node_color="gray")
plt.savefig("er1.pdf")

#4.3.4. Plotting Degree Distribution
def plot_degree_distribution(G):
    plt.hist(list(G.degree().values()), histtype="step")
    plt.xlabel("Degree $k$") #Number of conections
    plt.ylabel("$P(k)$") #Nodes
    plt.title("Degree distribution")

G1 = er_graph(500, 0.08)
plot_degree_distribution(G1)
G2 = er_graph(500, 0.08)
plot_degree_distribution(G2)
G3 = er_graph(500, 0.08)
plot_degree_distribution(G3)
plt.savefig("hist_3.pdf")

A = nx.erdos_renyi_graph(100, 0.03)
plot_degree_distribution(A)
B = nx.erdos_renyi_graph(100, 0.30)
plot_degree_distribution(B)
