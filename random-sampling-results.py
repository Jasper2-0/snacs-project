import os
import cPickle as pickle

def main():

resultsPicklePath = "/pickles/randomresults.pickle"
setupPicklePath = "/pickles/randomsetups.pickle"

setups = pickle.load(open(os.getcwd()+setupPicklePath,"rb"))
results = pickle.load(open(os.getcwd()+resultsPicklePath, "rb"))

datasets = listDataSets('/datasets/')

def listDataSets(directory):
    x = [x[1] for x in os.walk(os.getcwd()+directory)]
    return x[0]

main()
