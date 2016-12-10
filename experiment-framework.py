import os
import csv
import sys
import getopt

import networkx as nx
import numpy as np

from utilities import *

import cPickle as pickle

from random_sampling import RandomSampling
from pivot_selection import PivotSelection

def main(argv):

    setupName = ""
    setups = []
    results = []

    try:
        opts, args = getopt.getopt(sys.argv[1:],"s:",["setup"])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s","--setup"):
            setupName = arg;    

    #setup paths
    setupPicklePath = "/pickles/setups-"+setupName+".pickle"

    # load or resume experiments
    if os.path.isfile(os.getcwd()+"/pickles/inprogress/setups-"+setupName+".pickle"):
        setups = pickle.load(open(os.getcwd()+"/pickles/inprogress/setups-"+setupName+".pickle", "rb"))
        print "resuming from pickle"
    else:
        setups = load(setupPicklePath)

    #load in progress results
    if os.path.isfile(os.getcwd()+"/pickles/inprogress/results-"+setupName+".pickle"):
        print "loaded results from pickle"
        results = load("/pickles/inprogress/results-"+setupName+".pickle")
        
    
    nSetups = len(setups)

    # a bit hackish, but it works.
    if setupName.split("-")[0] == "randomsampling":
        graph = loadGraph(os.getcwd()+'/datasets/'+setupName.split("-")[1]+'/out.'+setupName.split("-")[1])
    if setupName.split("-")[0] == "pivot":
        graph = loadGraph(os.getcwd()+'/datasets/'+setupName.split("-")[2]+'/out.'+setupName.split("-")[2])

    i = 1;    

    inprogressFnSetups = os.getcwd()+"/pickles/inprogress/setups-"+setupName+".pickle"
    inprogressFnResults = os.getcwd()+"/pickles/inprogress/results-"+setupName+".pickle"

    while len(setups) > 0:
        s = {}
        s = setups.pop(0)
        experimentResults = {}
        
        print "running "+str(s['numberOfExperiments'])+" experiment(s): "+setupName.split("-")[0]+" "+str(i)+" of "+str(nSetups) + " with k="+str(s['k'])
        if setupName.split("-")[0] == "randomsampling":
            experimentResults = RandomSampling(graph,s['numberOfExperiments'],s['k'])
        if setupName.split("-")[0] == "pivot":
            experimentResults = PivotSelection(graph,s['numberOfExperiments'],s['k'],setupName.split("-")[1]);

        r = {}
        r['dataset'] = s['dataset'];
        r['setup'] = s;
        r['results'] = experimentResults
        results += [r]

        dump(setups,inprogressFnSetups);
        dump(results,inprogressFnResults)

        i += 1;

    #cleanup
    os.remove(inprogressFnSetups)
    os.remove(inprogressFnResults)
    dump(results,os.getcwd()+"/pickles/done/results-"+setupName+".pickle")
    #done!

if __name__ == "__main__":
    main(sys.argv[1:])