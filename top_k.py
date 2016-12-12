# -*- coding: utf-8 -*-
"""
Evaluation for finding top-k using estimations

@author: sebastiaan
"""
import networkx as nx
import numpy as np

def getActualTopK(Graph,topk):
    G = Graph
    avg_dists = np.zeros(len(G.nodes()))
    diameter = 0
    i = 0
    for v in G.nodes():
        lengths = nx.single_source_shortest_path_length(G,v)
        longest = np.max(lengths.values())
        if(longest > diameter):
            diameter = longest
        average = np.mean(lengths.values())
        avg_dists[i] = average
        i += 1
        
    print "diameter: " + str(diameter)
    
    sorted_nodes = np.argsort(avg_dists)
    return sorted_nodes[0:topk] 


def topkExperiment(Graph, numberOfExperiments, topk):
    G = Graph
    # Calculate actual average distance for all nodes
    actualTopK = getActualTopK(G,topk)
    print "actual top-" + str(topk) + ": " + str(actualTopK)
       
     
    """ some parameters """
    n = len(G.nodes())
    alpha = 1.0             # alpha >= 1
    L = np.arange(1,11)*5   # sample sizes    
    
    """ RUN FOR DIFFERENT SIZES OF l """
    for l in L:
        error = alpha * np.sqrt(np.log2(n)/l)
    
        """ CALCULATE ESIMATE FOR INTITAL SAMPLE size l """
        sample = np.random.choice(G.nodes(),l,replace=True)
    
        est_dists = np.zeros(n) # TODO: smarter, not reset at every iteration
        
        for u in sample:
            lengths = nx.single_source_shortest_path_length(G,u)
            for key, value in lengths.iteritems():
                est_dists[key] += value
    
        # Average cummulative distances
        est_dists = est_dists / l
    
        """ GET INITIAL CANDIDATE SET"""
         # sort on distances
        sorted_nodes = np.argsort(est_dists)
        v_k = sorted_nodes[topk-1]
        dist_k = est_dists[v_k]
        bound = dist_k + error # TODO: multiply with (upper bound of) diameter of graph
        is_candidate = np.zeros(n,np.bool)
        for u in range (0,n):
            if(est_dists[u] < bound):
                is_candidate[u] = True
        
        """ EVALUATE """
        print "sample set size:    " + str(l)
        print "candidate set size: " + str(sum(is_candidate))
        correctness = 0.0
        for u in actualTopK:
            if(is_candidate[u]):
                correctness += 1
        correctness /= topk
        print "correctness: " + str(correctness)
    
    
    
    
G = nx.
topkExperiment(G, 1, 3)
    