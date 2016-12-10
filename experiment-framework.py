import os
import csv

import networkx as nx
import numpy as np

import cPickle as pickle

from random_sampling import randomSamplingExperiment
from pivot_selection import pivotSelectionExperiment

def main():

    datasets = listDataSets('/datasets/')

    graphs = []

    for ds in datasets:
        graphs += [loadGraph(os.getcwd()+'/datasets/'+ds+'/out.'+ds)]

    print graphs

    results = {}

    for i in range(len(graphs)):

        #experimentResults = randomSamplingExperiment(graphs[i],numberOfExperiments = 1000,k = 1)
        # selectionMethod = 'RanDeg', 'MaxMin', or 'MaxSum'
        experimentResults = pivotSelectionExperiment(graphs[i],numberOfExperiments = 1000, k = 4, selectionMethod='MaxSum')
        
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
            G.add_edge(int(c[0])-1,int(c[1])-1); # nodes need to be ints, starting at 0 (NOTE: this is very bad practice)

    return G

def listDataSets(directory):
    x = [x[1] for x in os.walk(os.getcwd()+directory)]
    return x[0]

def dump(pickleVar, filename ):
    pickle.dump( pickleVar , open(filename,'wb'))

main()