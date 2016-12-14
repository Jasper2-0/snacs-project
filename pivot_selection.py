# -*- coding: utf-8 -*-
"""


@author: sebastiaan
"""
import networkx as nx
import numpy as np

""" 
select pivots randomly proportional to the degree 
"""
def selectRanDeg(Graph, k):
    G = Graph
    degrees = nx.degree(G).values()
    probs = np.divide(degrees,float(sum(degrees)))
    sample = np.random.choice(G.nodes(),k,replace=True,p=probs)
    return sample
    
"""
select pivots accordingly to MaxMin
"""
def selectMaxMin(Graph, k):
    G = Graph
    sample = np.zeros(k,dtype=np.int)
    # to keep track of distances
    allDistances = np.zeros(shape=(k,len(G.nodes())),dtype=np.int16)
    allDistances += int(1e3) # (sth. higher than the diameter, not too high because 16 bit ints)
    # first sample random
    v0 = np.random.choice(G.nodes())
    sample[0] = v0
    
    count = 1
    while(count < k):
        # calculate SSSP from last pivot
        distances = nx.single_source_shortest_path_length(G,sample[count-1])
        distances = distances.values()
        allDistances[count-1,:] = distances
        
        # MaxMin (maximum of minimum distances)
        minDists = np.amin(allDistances,axis=0)
        
        v_new = np.argmax(minDists)
        sample[count] = v_new
        
        count += 1
    
    return sample
    
"""
select pivots accordingly to MaxSum
"""
def selectMaxSum(Graph, k):
    G = Graph
    sample = np.zeros(k,dtype=np.int)
    # to keep track of distances
    allDistances = np.zeros(shape=(k,len(G.nodes())),dtype=np.int16)
    # first sample random
    v0 = np.random.choice(G.nodes())
    sample[0] = v0
    #print "v0: " + str(v0)
    
    count = 1
    while(count < k):
        # calculate SSSP from last pivot
        distances = nx.single_source_shortest_path_length(G,sample[count-1])
        distances = distances.values()
        allDistances[count-1,:] = distances
        
        # prevent selected pivots from being selected again
        for i in range(0,count):
            u = sample[i]
            allDistances[:,u] = 0
        
        # MaxSum (maximize sum of distances)
        sumDists = np.sum(allDistances,axis=0)
        v_new = np.argmax(sumDists)
        sample[count] = v_new
        #print "v"+ str(count) + ": " + str(v_new)
        
        count += 1
    
    return sample


def PivotSelection(Graph, numberOfExperiments, k, selectionMethod):
    G = Graph
    
    # Calculate actual average distance for all nodes
    avg_dists = np.zeros(len(G.nodes()))
    i = 0
    for v in G.nodes():
        lengths = nx.single_source_shortest_path_length(G,v)
        average = np.mean(lengths.values())
        avg_dists[i] = average
        i += 1
        
    # number of experiments
    exps = numberOfExperiments
    experiments = np.zeros(shape=(exps,len(G.nodes())))
    for i in range(0,exps):
        sample = np.zeros(k,dtype=np.int)
        # Estimate average distance (using k sample nodes)
        if (selectionMethod == 'RanDeg'):
            sample = selectRanDeg(G,k)
        elif (selectionMethod == 'MaxMin'):
            sample = selectMaxMin(G,k)
        elif (selectionMethod == 'MaxSum'):
            sample = selectMaxSum(G,k)
            
        est_dists = dict()
        # fill with 0
        for v in G.nodes():
            est_dists[v] = 0.0
            
        
        for u in sample:
            lengths = nx.single_source_shortest_path_length(G,u)
            for key, value in lengths.iteritems():
                est_dists[key] += value
                
        # Average cummulative distances
        for key, value in est_dists.iteritems():
            est_dists[key] = est_dists[key] / k
            
        experiments[i] = np.array(est_dists.values())
        
    
    # get performance of estimations
    AE_exp = 0.0
    AE_est = 0.0
    for j in range(0,len(G.nodes())):
        avg = np.mean(experiments[:,j])
        #std = np.std(experiments[:,j])
        AE_exp += np.abs(avg_dists[j] - avg)
        for i in range(0,exps):
            est = experiments[i,j]
            AE_est += np.abs(avg_dists[j] - est)
    
    MAE_exp = AE_exp / float(len(G.nodes()))
    MAE_est = AE_est / float(len(G.nodes())*exps)
        
    results = {}
    results['MAE (per experiment)'] = MAE_exp # accuracy (E[d] = d)
    results['MAE (for all estimates)'] = MAE_est # precision
    
    return results
        
        
            
        

        
        