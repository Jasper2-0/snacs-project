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
    i = 0
    for v in G.nodes():
        lengths = nx.single_source_shortest_path_length(G,v)
        average = np.mean(lengths.values())
        avg_dists[i] = average
        i += 1
    
    sorted_nodes = np.argsort(avg_dists)
    return sorted_nodes[0:topk] 


def topkExperiment(Graph, numberOfExperiments, topk):
    G = Graph
    # Calculate actual average distance for all nodes
    actualTopK = getActualTopK(G,topk)
    print actualTopK
    
    # TODO: Run paper algorithm
    
    
    # TODO: Compare with actual
    