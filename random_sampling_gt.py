# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 13:45:10 2016

@author: sebastiaan
"""
#import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from graph_tool.all import *
    

# Benchmark Graph
#G = nx.path_graph(10)
#nx.draw_circular(G)

def RandomSamplingGT(GTGraph, NXGraph, numberOfExperiments, k):
    # Calculate actual average distance for all nodes
    
    G = NXGraph
    GT = GTGraph
    
    # Calculate actual average distance for all nodes
    avg_dists = np.zeros(len(G.nodes()))
    i = 0
    for v in GT.vertices():
        lengths = heleSmerigeHack(graph_tool.topology.shortest_distance(GT,source=v).get_array())#nx.single_source_shortest_path_length(G,v)
        #print lengths
        average = np.mean(lengths.values())
        avg_dists[i] = average
        i += 1
        
    # number of experiments
    exps = numberOfExperiments
    experiments = np.zeros(shape=(exps,len(G.nodes())))
    for i in range(0,exps):
        # Estimate average distance (using k sample nodes)
        #k = 1 # we're getting k from the function now.
        sample = np.random.choice(G.nodes(),k,replace=True)
        est_dists = dict()
        # fill with 0
        for v in G.nodes():
            est_dists[v] = 0.0
        
        for u in sample:
            lengths = heleSmerigeHack(graph_tool.topology.shortest_distance(GT,source=u).get_array())
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
        
#    print "MAE (per experiment): " + str(MAE_exp)       # accuracy (E[d] = d)
#    print "MAE (for all estimates): " + str(MAE_est)    # precision

# Highly improper, but it should work...
# this converts the ouput from the gt-shortest path to the format of networkx's shortest path function...
def heleSmerigeHack(GTArray):
    d = {}
    nodeID = 0;
        
    for i in range(0,len(GTArray)):
        d[nodeID] = GTArray[i]
        nodeID += 1;
    
    return d