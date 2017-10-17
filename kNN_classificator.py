import numpy as np

def distance(p1, p2):
    """Find distance between points p1 and p2.
    p1 and p2 must be numpy arrays."""
    return np.sqrt(np.sum(np.power(p2 - p1, 2)))

import random

def majority_vote(votes):
    """
    Return the most common element in votes
    """
    vote_counts = {}
    for vote in votes:
        if vote in vote_counts:
            vote_counts[vote] += 1
        else:
            vote_counts[vote] = 1
    
    winners = []
    max_count = max(vote_counts.values())
    for vote, count in vote_counts.items():
        if count == max_count:
            winners.append(vote)
        
    return random.choice(winners)

import scipy.stats as ss

def majority_vote_short(votes):
    """
    Return the most common element in votes.
    """
    mode, count = ss.mstats.mode(votes)
        
    return mode

def find_nearest_neighbors(p, points, k=5):
    """Findthe k nearest neighbors of point p and return their indices"""
    distances = np.zeros(points.shape[0])
    for i in range(len(distances)):
        distances[i] = distance(p, points[i])
    ind = np.argsort(distances)
    return ind[0:k]

def knn_predict(p, points, outcomes, k=5):
    ind = find_nearest_neighbors(p, points, k)
    return majority_vote(outcomes[ind])

def generate_synth_data(n=50):
    """Create two sets of points from bivariate normal distributions."""
    points = np.concatenate((ss.norm(0,1).rvs((n,2)), ss.norm(1,1).rvs((n,2))),axis=0)
    outcomes =  np.concatenate((np.repeat(0,n), np.repeat(1,n)))
    return (points, outcomes)
#import numpy as np
#import matplotlib.pyplot as plt
#import scipy.stats as ss
#n = 20
#(points, outcomes) = generate_synth_data(n)
#plt.figure()
#plt.plot(points[:n,0], points[:n,1], "ro")
#plt.plot(points[n:,0], points[n:,1], "bo")
#plt.savefig("bivardata.pdf")


def make_prediction_grid(predictors, outcomes, limits, h, k):
    """Classify each point on the prediction grid."""
    (x_min, x_max, y_min, y_max) = limits
    xs = np.arange(x_min, x_max, h)
    ys = np.arange(y_min, y_max, h)
    xx, yy = np.meshgrid(xs, ys)
    
    prediction_grid = np.zeros(xx.shape, dtype=int)
    for i,x in enumerate(xs):
        for j,y in enumerate(ys):
            p = np.array([x,y])
            prediction_grid[i,j] = knn_predict(p, predictors, outcomes, k)
        
    return (xx, yy, prediction_grid)

#Ejemplo: Flores de Ron Fischer

from sklearn import datasets

iris = datasets.load_iris()
predictors = iris.data[:, 0:2]
outcomes = iris.target
plt.plot(predictors[outcomes==0][:,0],predictors[outcomes==0][:,1], "ro")
plt.plot(predictors[outcomes==1][:,0],predictors[outcomes==1][:,1], "go")
plt.plot(predictors[outcomes==2][:,0],predictors[outcomes==2][:,1], "bo")
plt.savefig("iris.pdf")


k=5; filename="iris_grid.pdf"; limits = (4,8,0.5,4.5); h=0.1
(xx, yy, prediction_grid) = make_prediction_grid(predictors, outcomes, limits, h, k)
plot_prediction_grid(xx, yy, prediction_grid, filename)

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(predictors, outcomes)
sk_predictions = knn.predict(predictors)
my_predictions = np.array([knn_predict(p, predictors, outcomes, 5) for p in predictors])
#para probar si los métodos coinciden
print(100*np.mean(sk_predictions == my_predictions))
#los dos modelos concuerdan con las observaciones?
print(100*np.mean(sk_predictions == outcomes))
print(100*np.mean(my_predictions == outcomes)) #This one performs a bit better

