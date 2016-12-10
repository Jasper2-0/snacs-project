import os
import csv

import networkx as nx
import numpy as np

import cPickle as pickle

from random_sampling import randomSamplingExperiment



def main():

    datasets = listDataSets('/datasets/')
    setupPicklePath = "/pickles/randomsetups.pickle"
    resultsPicklePath = "/pickles/randomresults.pickle"

    graphs = []
    setups = []
    results = []
    
    experimentSize = 1000
    
    
    # load graphs
    for ds in datasets:
        graphs += [loadGraph(os.getcwd()+'/datasets/'+ds+'/out.'+ds)]
    
    
    os.getcwd()+setupPicklePath
    
    # load or generate experiments
    if os.path.isfile(os.getcwd()+setupPicklePath):
        setups = pickle.load(open(os.getcwd()+setupPicklePath, "rb"))
        print "loaded setups from pickle"
    else:
        for i in range(len(graphs)):
            setups+= generateSetupsRandomSampling(datasets[i],graphs[i],experimentSize)
            dump(setups,os.getcwd()+setupPicklePath)

    #load results
    if os.path.isfile(os.getcwd()+resultsPicklePath):
        print "loaded results from pickle"
        results = pickle.load(open(os.getcwd()+resultsPicklePath,"rb"))

    i = 1;
    nSetups = len(setups)
    
    while len(setups) > 0:
        s = setups.pop(0)
        
        print "running experiment: "+str(i)+" of "+str(nSetups)

        experimentResults = randomSamplingExperiment(graphs[datasets.index(s['dataset'])],s['numberOfExperiments'],s['k'])

        r = {}
        r['dataset'] = s['dataset'];
        r['setup'] = s;
        r['results'] = experimentResults
        results += [r]
        
        dump(setups,os.getcwd()+setupPicklePath)
        dump(results,os.getcwd()+resultsPicklePath)
        
        i += 1;

def loadGraph(filename):
    G = nx.Graph()

    with open(filename,'r') as edgeFile:
        fileReader = csv.reader(edgeFile, delimiter=' ', quotechar='|')

        fileReader.next() # skip header row 1 & 2
        fileReader.next()

        for c in fileReader:
            G.add_edge(c[0],c[1]);

    return G


def generateSetupsRandomSampling(dataset, G,nExperiments):
    
    n = G.number_of_nodes()

    # generate k samples
    kSamples = []
    
    if n > 100:
        kSamples = []
        
        for i in range(1,101):
            kSamples += [i]

        for i in range(100,n,100):
            kSamples += [i]
        kSamples += [n]
    else:
        for i in range(1,n+1):
            kSamples += [i]

    experiments = []

    for k in kSamples:
        exp = {};
        exp['dataset'] = dataset;
        exp['k'] = k
        exp['numberOfExperiments'] = nExperiments
        experiments += [exp]

    return experiments

def listDataSets(directory):
    x = [x[1] for x in os.walk(os.getcwd()+directory)]
    return x[0]

def dump(pickleVar, filename ):
    pickle.dump( pickleVar , open(filename,'wb'))

main()