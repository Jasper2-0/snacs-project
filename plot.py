import os
import csv
import sys
import getopt

import numpy as np

from utilities import *

import cPickle as pickle

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt





def main(argv):

    resultName = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:],"r:",["results"])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-r","--results"):
            plot(arg)

def plot(resultsName):

    results = pickle.load(open(os.getcwd()+"/pickles/done/results-"+resultsName+".pickle", "rb"))

    k = []
    mae = []

    for r in results:
        k += [r['setup']['k']];
        mae += [r['results']['MAE (for all estimates)']]
    
    k = np.asarray(k)
    mae = np.array(mae)
    
    print k.max()
    print mae.max()
    
    plt.scatter(k,mae,linewidths=0.0)
    plt.grid()
    plt.ylim(ymin=-1.0)
    plt.ylim(ymax=5.0)
    plt.xlim(xmin=0.0)
    plt.xlim(xmax=6000)
    plt.ylabel("MAE (for all estimates )")
    plt.xlabel("k")
    plt.xscale('symlog')
    plt.title(resultsName)
    plt.savefig("diagrams/"+resultsName+".pdf")
    plt.clf();

    
def plotk(resultsName):
    results = pickle.load(open(os.getcwd()+"/pickles/done/results-"+resultsName+".pickle", "rb"))

    print results

    k = []
    
#    mae = []

#    for r in results:
#        k += [r['setup']['k']];
#        mae += [r['results']['MAE (for all estimates)']]
#    
#    k = np.asarray(k)
#    mae = np.array(mae)
#    
#    print k.max()
#    print mae.max()
#    
#    plt.scatter(k,mae,linewidths=0.0)
#    plt.grid()
#    plt.ylim(ymin=-1.0)
#    plt.ylim(ymax=5.0)
#    plt.xlim(xmin=0.0)
#    plt.xlim(xmax=6000)
#    plt.ylabel("MAE (for all estimates )")
#    plt.xlabel("k")
#    plt.xscale('symlog')
#    plt.title(resultsName)
#    plt.savefig("diagrams/"+resultsName+".pdf")
#    plt.clf();

if __name__ == "__main__":
    main(sys.argv[1:])