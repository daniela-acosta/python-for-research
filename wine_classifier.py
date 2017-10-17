#Ejercicio 1. Extraer data de internet
import pandas as pd
data = pd.read_csv('https://s3.amazonaws.com/demo-datasets/wine.csv')

#Ejercicio 2. Eliminar columna redundante
numeric_data = data.drop("color",axis=1)

#Ejercicio 3. Estandarizar datos y encontrar los dos componentes principales más informativos
import numpy as np
numeric_data = (numeric_data-np.mean(numeric_data,axis=0))/np.std(numeric_data,axis=0)
# Nota: También se puede hacer con pandas --> numeric_data.mean() y numeric_data.std()

import sklearn.decomposition
pca = sklearn.decomposition.PCA(n_components=2)
principal_components = pca.fit(numeric_data).transform(numeric_data)

#Ejercicio 4. Graficar puntos en los dos componentes principales
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_pdf import PdfPages
observation_colormap = ListedColormap(['red', 'blue'])
x = principal_components[:,0]
y = principal_components[:,1]

plt.title("Principal Components of Wine")
plt.scatter(x, y, alpha = 0.2,
    c = data['high_quality'], cmap = observation_colormap, edgecolors = 'none')
plt.xlim(-8, 8); plt.ylim(-8, 8)
plt.xlabel("Principal Component 1"); plt.ylabel("Principal Component 2")
plt.show()

#Ejercicio 5. Función para ver qué tanto coinciden predcciones con observaciones
def accuracy(predictions, outcomes):
    return 100*np.mean(predictions == outcomes)

#Ejercicio 6. Encontrar el porcentaje de vinos de mala calidad
print(accuracy(0,data["high_quality"]))

#Ejercicio 7. Usar el paquete scikitlearn para encontrar las predicciones de vinos malos con knn
# y ver qué tan certero es, usando accuracy
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(numeric_data, data['high_quality'])
library_predictions = knn.predict(numeric_data)
print(accuracy(library_predictions,data["high_quality"]))

#Ejercicio 8. Our homemade kNN classifier does not take any shortcuts in calculating which neighbors 
#are closest to each observation, so it is likely too slow to carry out on the whole dataset. 
#To circumvent this, fix the random generator using:
import random
n_rows = data.shape[0]
random.seed(123)
selection = random.sample(range(n_rows), 10)

#Ejercicio 9. Usando nuestro modelo knn, predecir si los vinos son de alta calidad y calcular
#el porcentaje de error
predictors = np.array(numeric_data)
training_indices = [i for i in range(len(predictors)) if i not in selection]
outcomes = np.array(data["high_quality"])

my_p = []
for p in predictors[selection]:
    my_p.append(knn_predict(p, predictors[training_indices,:], outcomes, k=5))
    
my_predictions = np.array(my_p)
percentage = accuracy(my_predictions,data.high_quality[selection])
print(percentage)
