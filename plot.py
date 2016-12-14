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
    
    plt.scatter(k,mae,linewidths=0.0,edgecolors=None)
    plt.grid()
    plt.ylim(ymin=-1.0)
    plt.ylim(ymax=6.0)
    plt.xlim(xmin=0.0)
    plt.xlim(xmax=6000)
    plt.ylabel("MAE (for all estimates )")
    plt.xlabel("k")
    plt.xscale('symlog')
    plt.title(resultsName)
    plt.savefig("diagrams/"+resultsName+".pdf",bbox_inches='tight')
    plt.clf();


def plotAnim(resultsName):
    results = pickle.load(open(os.getcwd()+"/pickles/done/results-"+resultsName+".pickle", "rb"))
    
    #print len(results)
    
    for i in range(0,len(results)):
        plotk(resultsName,i)

def plotk(resultsName, kIndex):
    results = pickle.load(open(os.getcwd()+"/pickles/done/results-"+resultsName+".pickle", "rb"))


    #kIndex = kIndex # so k = 50

    sampleSize = []
    accs = []

    #print kIndex
    
    k = results[kIndex]['setup']['k']
    
    for r in results[kIndex]['results']:
        sampleSize += [r['sample size']]
        accs += [r['avg. candidate set size']]
    
    accs = np.asarray(accs)
    sampleSize = np.asarray(sampleSize)
    
    #print accs.max();
    #print sampleSize.max()
    
    plt.scatter(sampleSize,accs,linewidths=0.0,edgecolors=None)
    plt.grid()
    plt.ylim(ymin=0.0)
    plt.ylim(ymax=900.0)
    plt.xlim(xmin=0.0)
    plt.xlim(xmax=1100)
    plt.ylabel("Avg. Candidate Set Size")
    plt.xlabel("Samples")
    #plt.xscale('symlog')
    plt.title(resultsName +" for k = "+str(k))
    plt.savefig("diagrams/topk-pdfs/"+resultsName+"/"+resultsName+"_k"+str(k).zfill(4)+".pdf",bbox_inches='tight',dpi=150)
    plt.clf();

if __name__ == "__main__":
    main(sys.argv[1:])