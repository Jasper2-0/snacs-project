#!/usr/local/bin/python

from utilities import *

def main():
    
    datasets = listDataSets('/datasets/')
    setupPicklePath = "/pickles/randomsetups.pickle"

    graphs = []
    setups = []

    pivots = ['MaxMin','MaxSum','RanDeg']

    experimentSize = 20

    # load graphs
    for ds in datasets:
        graphs += [loadGraph(os.getcwd()+'/datasets/'+ds+'/out.'+ds)]

    for i in range(len(graphs)):
        setups = generateSetupsRandomSampling(datasets[i],graphs[i],experimentSize)
        dump(setups,os.getcwd()+"/pickles/setups/setups-randomsampling-"+datasets[i]+".pickle")
        
        for method in pivots:
            setups = generateSetupsPivot(datasets[i],graphs[i],experimentSize,method)
            dump(setups,os.getcwd()+"/pickles/setups/setups-pivot-"+method+"-"+datasets[i]+".pickle")



def createkSamples(n):
    # generate k samples
    kSamples = []

    if n > 100:

        for i in range(1,101):
            kSamples += [i]

        for i in range(101,n,100):
            kSamples += [i]
        kSamples += [n]
    else:
        for i in range(1,n+1):
            kSamples += [i]
    
    return kSamples

def generateSetupsRandomSampling(dataset, G,nExperiments):

    largest = max(nx.connected_component_subgraphs(G), key=len)
    largest = nx.convert_node_labels_to_integers(G)

    n = largest.number_of_nodes()


    experiments = []

    for k in createkSamples(n):
        exp = {};
        exp['dataset'] = dataset;
        exp['k'] = k
        exp['numberOfExperiments'] = nExperiments
        experiments += [exp]

    return experiments

def generateSetupsPivot(dataset, G,nExperiments,selectionMethod):

    largest = max(nx.connected_component_subgraphs(G), key=len)
    largest = nx.convert_node_labels_to_integers(G)

    n = largest.number_of_nodes()

    experiments = []

    for k in createkSamples(n):
        exp = {};
        exp['dataset'] = dataset;
        exp['k'] = k
        exp['numberOfExperiments'] = nExperiments
        exp['selectionMethod'] = selectionMethod
        experiments += [exp]

    return experiments

if __name__ == "__main__":
    main()