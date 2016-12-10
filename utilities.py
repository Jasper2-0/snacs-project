import os
import csv

import networkx as nx
import cPickle as pickle

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

def load(path):
    return pickle.load(open(os.getcwd()+path,"rb"))
