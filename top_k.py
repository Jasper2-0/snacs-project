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
        
    #print "diameter: " + str(diameter)
    
    sorted_nodes = np.argsort(avg_dists)
    return sorted_nodes[0:topk] 


def topkExperiment(Graph, numberOfExperiments, topk):
    G = Graph
    # Calculate actual average distance for all nodes
    actualTopK = getActualTopK(G,topk)
    #print "actual top-" + str(topk) + ": " + str(actualTopK)
       
     
    """ some parameters """
    n = len(G.nodes())
    diam_upper_bound = n
    alpha = 0.15             # alpha >= 1 in theory, but yeah...
    step = 100               # should depend on size of graph but since our graphs are roughly the same size
    L = np.arange(1,11)*step # sample sizes (from 100 to 1000 atm)
    
    candidate_sizes = np.zeros(len(L),dtype=np.int)
    correctness_for_l = np.zeros(len(L))
    """ <EXPERIMENT> """
    for exp in range(0,numberOfExperiments):
        sum_dists = np.zeros(n)
        
        """ RUN FOR DIFFERENT SIZES OF l """
        index_l = 0
        for l in L:
            error = alpha * np.sqrt(np.log10(n)/l)
        
            """ CALCULATE ESIMATE FOR INTITAL SAMPLE size l """
            sample = np.random.choice(G.nodes(),step,replace=True)
            
            for u in sample:
                lengths = nx.single_source_shortest_path_length(G,u)
                for key, value in lengths.iteritems():
                    sum_dists[key] += value
                # get longest path length for lower bound of diameter
                longest = max(lengths.values())
                if(2*longest < diam_upper_bound):
                    diam_upper_bound = 2*longest
        
            # Average cummulative distances
            est_dists = sum_dists / l
        
            """ GET INITIAL CANDIDATE SET"""
             # sort on distances
            sorted_nodes = np.argsort(est_dists)
            v_k = sorted_nodes[topk-1]
            dist_k = est_dists[v_k]
            bound = dist_k + error*diam_upper_bound
            is_candidate = np.zeros(n,np.bool)
            for u in range (0,n):
                if(est_dists[u] < bound):
                    is_candidate[u] = True
            
            """ EVALUATE """
            candidate_sizes[index_l] += sum(is_candidate)
            correctness = 0.0
            for u in actualTopK:
                if(is_candidate[u]):
                    correctness += 1
            correctness /= topk
            correctness_for_l[index_l] += correctness 
            index_l += 1
    """ </EXPERIMENT> """
    
    """ RESULTS """
    candidate_sizes /= numberOfExperiments
    correctness_for_l /= numberOfExperiments
    results = np.empty(len(L),dtype=object)
    for i in range(0,len(L)):
        result = {}
        result['sample size'] = L[i]
        result['avg. candidate set size'] = candidate_sizes[i]
        result['avg. correctness'] = correctness_for_l[i]
        results[i] = result
        
    return results
    
    
#G = nx.karate_club_graph()
#G = nx.convert_node_labels_to_integers(nx.davis_southern_women_graph())
#G = nx.convert_node_labels_to_integers(nx.florentine_families_graph())
#G = nx.gnp_random_graph(100,0.4)
#G = nx.path_graph(10)
#print topkExperiment(G, 20, 3)



