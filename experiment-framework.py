import os
import csv

import networkx as nx
import numpy as np

import cPickle as pickle

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

    for i in range(len(graphs)):

        experimentResults = randomSamplingExperiment(graphs[i],numberOfExperiments = 1000,k = 1)
        
        results[datasets[i]] = experimentResults

    dump(results,'pickles/results.pickle')

    print results

def loadGraph(filename):
    G = nx.Graph()

    with open(filename,'r') as edgeFile:
        fileReader = csv.reader(edgeFile, delimiter=' ', quotechar='|')

        fileReader.next() # skip header row 1 & 2
        fileReader.next()

        for c in fileReader:
            G.add_edge(c[0],c[1]);
            
    return G

def listDataSets(directory):
    x = [x[1] for x in os.walk(os.getcwd()+directory)]
    return x[0]

def dump(pickleVar, filename ):
    pickle.dump( pickleVar , open(filename,'wb'))

main()