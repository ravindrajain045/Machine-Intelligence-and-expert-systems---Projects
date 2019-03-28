import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import random


def k_means_clustering(df, cluster_dist):
    #error for different k values
    error = pd.DataFrame({
        '2': [0],
        '3': [0],
        '4': [0],
        '5': [0],
        '6': [0]
    })
    
    np.random.seed(200)
    for k in range(2,7):
        # centroids[i] = [x, y]
        centroids = {i+1: [random.uniform(-0.3, 4.0), random.uniform(-1.4, 2.0)] for i in range(k)}
        plt.scatter(df['x'], df['y'], color='k', alpha=0.3)
        colmap = {1: 'r', 2: 'g', 3: 'b', 4: 'm', 5: 'y', 6: 'k'}
        for i in centroids.keys():
            plt.scatter(*centroids[i], color=colmap[i])
        plt.xlim(-1, 5)
        plt.ylim(-2, 3)
        plt.show()
        
        ## Assignment Stage
        
        def assignment(df, centroids):
            for i in centroids.keys():
                if cluster_dist == 'euclidean':
                    df['distance_from_{}'.format(i)] = (np.sqrt((df['x'] - centroids[i][0]) ** 2 + (df['y'] - centroids[i][1]) ** 2))
                if cluster_dist == 'cosine':
                    df['distance_from_{}'.format(i)] = 1- ((df['x'] * centroids[i][0]) + (df['y'] * centroids[i][1]))/(np.sqrt((df['x']) ** 2+df['y'] ** 2)*np.sqrt((centroids[i][0]) ** 2 + (centroids[i][1]) ** 2))
            centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
            df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)
            df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
            df['color'] = df['closest'].map(lambda x: colmap[x])
            return df
        
        df = assignment(df, centroids)
        
        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.2, edgecolor='k')
        for i in centroids.keys():
            plt.scatter(*centroids[i], color=colmap[i])
        plt.xlim(-1, 5)
        plt.ylim(-2, 3)
        plt.show()
        
        ## Update Stage
        def update(k):
            for i in centroids.keys():
                centroids[i][0] = np.mean(df[df['closest'] == i]['x'])
                centroids[i][1] = np.mean(df[df['closest'] == i]['y'])
            return k
        
        centroids = update(centroids)
        	    
        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.2, edgecolor='k')
        for i in centroids.keys():
            plt.scatter(*centroids[i], color=colmap[i])
        plt.xlim(-1, 5)
        plt.ylim(-2, 3)
        plt.show()
        
        ## Repeat Assigment Stage
        
        df = assignment(df, centroids)
        
        # Plot results
        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.2, edgecolor='k')
        for i in centroids.keys():
            plt.scatter(*centroids[i], color=colmap[i])
        plt.xlim(-1, 5)
        plt.ylim(-2, 3)
        plt.show()
        
        # Continue until all assigned categories don't change any more
        while True:
            closest_centroids = df['closest'].copy(deep=True)
            centroids = update(centroids)
            df = assignment(df, centroids)
            if closest_centroids.equals(df['closest']):
                break
        
            plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.2, edgecolor='k')
            for i in centroids.keys():
                plt.scatter(*centroids[i], color=colmap[i])
            plt.xlim(-1, 5)
            plt.ylim(-2, 3)
            plt.show()
        
        #calculating Error 
        for i in range(len(df.index)):
            error['{}'.format(k)] += df['distance_from_{}'.format(df['closest'][i])][i]
    
    error_plot_dist = pd.DataFrame({
        'x': [k for k in range(2,7)],
        'y': [error['{}'.format(k)] for k in range(2,7)]
    })
    return error_plot_dist


a = sio.loadmat('data.mat')
data=a['h']
df = pd.DataFrame(data,columns=list('xy'))

error_plot_euclidean_dist = k_means_clustering(df, 'euclidean')

error_plot_cosine_dist = k_means_clustering(df, 'cosine')

plt.plot(error_plot_euclidean_dist['x'], error_plot_euclidean_dist['y'], color='b',marker='o')
plt.plot(error_plot_cosine_dist['x'], error_plot_cosine_dist['y'], color='r',marker='o')
plt.show()
	



