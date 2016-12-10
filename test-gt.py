#!/usr/local/bin/python

import os
import csv
import sys
import getopt

import networkx as nx
import numpy as np

from utilities import *

import cPickle as pickle

from random_sampling_debug_gt import RandomSampling
from random_sampling_gt import RandomSamplingGT

def main(argv):
    
    setupName = ""
    setups = []
    resultsGT = []
    resultsNX = []
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"s:",["setup"])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s","--setup"):
            setupName = arg;    

    #setup paths
    setupPicklePath = "/pickles/setups-"+setupName+".pickle"
    
    setups = load(setupPicklePath)

    nSetups = len(setups)

    # a bit hackish, but it works.
    if setupName.split("-")[0] == "randomsampling":
        graph = loadGraph(os.getcwd()+'/datasets/'+setupName.split("-")[1]+'/out.'+setupName.split("-")[1])
        graphGT = loadGraphGT(os.getcwd()+'/datasets/'+setupName.split("-")[1]+'/out.'+setupName.split("-")[1])

    i = 1;    

    while len(setups) > 0:
        s = {}
        s = setups.pop(0)
        experimentResultsGT = {}
        experimentResultsNX = {}
        
        print "running "+str(s['numberOfExperiments'])+" experiment(s): "+setupName.split("-")[0]+" "+str(i)+" of "+str(nSetups) + " with k="+str(s['k'])
        if setupName.split("-")[0] == "randomsampling":
            print "GT"
            experimentResultsGT = RandomSamplingGT(graphGT,graph,s['numberOfExperiments'],s['k'])
            print "NX"
            experimentResultsNX = RandomSampling(graph,s['numberOfExperiments'],s['k'])

        rGT = {}
        rGT['dataset'] = s['dataset'];
        rGT['setup'] = s;
        rGT['results'] = experimentResultsGT
        resultsGT += [rGT]

        rNX = {}
        rNX['dataset'] = s['dataset'];
        rNX['setup'] = s;
        rNX['results'] = experimentResultsNX
        resultsNX += [rNX]


        i += 1;

    #cleanup
    print resultsGT
    print resultsNX

if __name__ == "__main__":
    main(sys.argv[1:]) 