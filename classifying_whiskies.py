import numpy as np
import pandas as pd

whisky = pd.read_csv("whiskies.txt")
whisky["Region"] = pd.read_csv("regions.txt")
flavors = whisky[:, 2:14]

#Correlation between different flavors
corr_flavors = pd.DataFrame.corr(flavors)
import matplotlib.pyplot as plt
plt.figure(figsize=(10,10))
plt.pcolor(corr_flavors)
plt.colorbar()
plt.savefig("corr_flavors.pdf")
#Correlation between individual whiskies
corr_whisky = pd.DataFrame.corr(flavors.transpose())
plt.figure(figsize=(10,10))
plt.pcolor(corr_whisky)
plt.axis("tight")
plt.colorbar()
plt.savefig("corr_whisky.pdf")

#Encontrar clusters de whiskies (6)
from sklearn.cluster.bicluster import SpectralCoclustering
model = SpectralCoclustering(n_clusters=6, random_state=0)
model.fit(corr_whisky)
np.sum(model.rows_, axis=1) #this tells how many whiskies blong in each cluster
np.sum(model.rows_, axis=0) #this tells how many clusters blong in each observation. Everything has to be = 1
model.row_labels_ #Tells to what cluster belongs each observation

#Especificar los clusters de cada whisky
whisky["Group"] = pd.Series(model.row_labels_, index=whisky.index) #Add group to table
whisky = whisky.ix[np.argsort(model.row_labels_)] #we order the whole table by increasing number of group
whisky = whisky.reset_index(drop=True)#reset index of the DataFrame
correlations = pd.DataFrame.corr(whisky.iloc[:,2:14].transpose())#recalculate the corr matrix
correlations = np.array(correlations)

#Plotting these correlations
plt.figure(figsize = (14,7))
plt.subplot(121)
plt.pcolor(corr_whisky)
plt.title("Original")
plt.axis("tight")
plt.subplot(122)
plt.pcolor(correlations)
plt.title("Rearranged")
plt.axis("tight")
plt.savefig("correlations.pdf")