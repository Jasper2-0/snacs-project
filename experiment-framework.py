import os
import csv

import networkx as nx
import numpy as np

from random_sampling import randomSamplingExperiment

def main():

    datasets = listDataSets('/datasets/')

    paths = []
    for ds in datasets:
        paths+= [os.getcwd()+'/datasets/'+ds+'/out.'+ds]

    graphs = []

    for path in paths:
        graphs += [loadGraph(path)]

    results = {}

    for g in graphs:
        

    print randomSamplingExperiment(graphs[5],numberOfExperiments = 1000,k = 1)

def loadGraph(filename):
    G = nx.Graph()

    with open(filename,'r') as edgeFile:
        fileReader = csv.reader(edgeFile, delimiter=' ', quotechar='|')

        fileReader.next() # skip header 1 & 2
        fileReader.next()

        for c in fileReader:
            G.add_edge(c[0],c[1]);
            
    return G

def listDataSets(directory):
    x = [x[1] for x in os.walk(os.getcwd()+directory)]
    return x[0]

main()