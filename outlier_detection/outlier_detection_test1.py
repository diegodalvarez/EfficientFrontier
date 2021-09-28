import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

df = pd.read_csv("results_frame_test.csv", index_col = 0)
df = df.to_numpy()

#plt.scatter(df.ret, df.stdev)

cluster_size = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

for j in range(len(cluster_size)):

    print(cluster_size[j])    
    km = KMeans(n_clusters = cluster_size[j])
    clusters = km.fit_predict(df)
    cluster_title = cluster_size[j]
    
    '''
    fig = plt.figure()
    plt.scatter(*zip(*df), c = clusters)
    plt.show()
    '''

    centroids = km.cluster_centers_
    # points array will be used to reach the index easy
    points = np.empty((0,len(df[0])), float)
    # distances will be used to calculate outliers
    distances = np.empty((0,len(df[0])), float)
    # getting points and distances
    for i, center_elem in enumerate(centroids):
        # cdist is used to calculate the distance between center and other points
        distances = np.append(distances, cdist([center_elem],df[clusters == i], 'euclidean')) 
        points = np.append(points, df[clusters == i], axis=0)
    
    percentiles = [99.1, 99.2, 99.3, 99.4, 99.5, 99.6, 99.7, 99.8, 99.9]
    
    for i in range(len(percentiles)):
        
        print(percentiles[i])
        percentile = percentiles[i]
        # getting outliers whose distances are greater than some percentile
        outliers = points[np.where(distances > np.percentile(distances, percentile))]
        
        fig = plt.figure()
        # plotting initial df
        plt.scatter(*zip(*df),c=clusters) 
        # plotting red ovals around outlier points
        plt.scatter(*zip(*outliers), marker = 'o' , facecolor = 'none',edgecolor= "r",s=70);
        # plotting centers as blue dots
        plt.scatter(*zip(*centroids),marker= 'o',facecolor='b',edgecolor='b',s=10);
        plt.title(percentiles[i])
        plt.show()

