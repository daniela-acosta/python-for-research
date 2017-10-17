"""Network homophily occurs when nodes that share an edge share a 
characteristic more often than nodes that do not share an edge. In this case 
study, we will investigate homophily of several characteristics of individuals 
connected in social networks in rural India"""

import pandas as pd
#Ejercicio 1. Leer archivo y tomar datos de solo las aldeas 1 y 2
data_filepath = "https://s3.amazonaws.com/assets.datacamp.com/production/course_974/datasets/"
df  = pd.read_stata(data_filepath + "individual_characteristics.dta")
df1 = df[df["village"] == 1]
df2 = df[df["village"] == 2]

#Ejercicio 2. ID ó PID de cada habitante
pid1 = pd.read_csv(data_filepath + "key_vilno_1.csv", header=None)
pid2 = pd.read_csv(data_filepath + "key_vilno_2.csv", header=None)

#Ejercicio 3. Diccionarios para sexo, casta, y religión correspondieno al id de cada habitante
sex1 = df1["resp_gend"].to_dict()
sex1 = dict((df1["pid"][key], value) for (key, value) in sex1.items())
caste1 = df1["caste"].to_dict()
caste1 = dict((df1["pid"][key], value) for (key, value) in caste1.items())
religion1 = df1["religion"].to_dict()
religion1 = dict((df1["pid"][key], value) for (key, value) in religion1.items())
sex2 = df2["resp_gend"].to_dict()
sex2 = dict((df2["pid"][key], value) for (key, value) in sex2.items())
caste2 = df2["caste"].to_dict()
caste2 = dict((df2["pid"][key], value) for (key, value) in caste2.items())
religion2 = df2["religion"].to_dict()
religion2 = dict((df2["pid"][key], value) for (key, value) in religion2.items())

#Ejercicio 4 y 5. Cálculo de probabilidad de homofilia para cierta característica
#Ésta se calcula como la suma de los cuadrados de las frecuencias de las opciones de dicha característica
from collections import Counter
def chance_homophily(chars):
    valores = Counter(chars.values()).values()
    total = sum(valores)
    fracc_sq = []
    for i in valores:
        fracc_sq.append((i/total)**2)
    return sum(fracc_sq)

print("Village 1 chance of same sex:", chance_homophily(sex1))
print("Village 1 chance of same caste:", chance_homophily(caste1))
print("Village 1 chance of same religion:", chance_homophily(religion1))
print("Village 2 chance of same sex:", chance_homophily(sex2))
print("Village 2 chance of same caste:", chance_homophily(caste2))
print("Village 2 chance of same religion:", chance_homophily(religion2))

#Ejercicio 6 y /. Cálculo de Homofilia para una red (fracción de pares de nodos conectados que comparten una característica)
def homophily(G, chars, IDs):
    """
    Given a network G, a dict of characteristics chars for node IDs,
    and dict of node IDs for each node in the network,
    find the homophily of the network.
    """
    num_same_ties, num_ties = 0, 0
    for n1 in G.nodes():
        for n2 in G.nodes():
            if n1 > n2:   # do not double-count edges!
                if IDs[n1] in chars and IDs[n2] in chars:
                    if G.has_edge(n1, n2):
                        num_ties += 1
                        if chars[IDs[n1]] == chars[IDs[n2]]:
                            num_same_ties += 1
    return (num_same_ties / num_ties)

print("Village 1 observed proportion of same sex:", homophily(G1, sex1, pid1))
print("Village 1 observed proportion of same caste:", homophily(G1, caste1, pid1))
print("Village 1 observed proportion of same religion:", homophily(G1, religion1, pid1))
print("Village 2 observed proportion of same sex:", homophily(G2, sex2, pid2))
print("Village 2 observed proportion of same caste:", homophily(G2, caste2, pid2))
print("Village 2 observed proportion of same religion:", homophily(G2, religion2, pid2))

#Conclusión: En India, es más probable que dos individuos se relacionen si comparten religión, seguido de casta y terminando con género
