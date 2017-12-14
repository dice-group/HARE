import numpy as np
from Computations.hare_scripts import hare
from Computations.pagerank_scripts import pagerank

repetitions = 5
dataset = ["Airports", "dbpedia", "dogfood", "LUBM/L20", "LUBM/L50", "LUBM/L100", "LUBM/L200", "LUBM/L500",
           "LUBM/L1000", "sec", "sider", "UPSTO"]
for data in dataset:

    data = "Data/Matrices/HARE/" + data
    print("WITH: ", data)
    # parseRDF(data)
    # getTransitionMatrices(data)

    print(".....HARE.....")
    runtimes_hare = np.array(repetitions * [.0])
    for i in range(repetitions - 1):
        runtime = hare(data, epsilon=10 ** (-2), damping=.85, saveresults=False, printerror=False, printruntimes=False)
        runtimes_hare[i] = runtime
    print("Average Runtime HARE: ", np.mean(runtimes_hare))

    print(".....PAGERANK.....")
    runtimes_pagerank = np.array(repetitions * [.0])
    for i in range(repetitions):
        runtime = pagerank(data, epsilon=10 ** (-3), damping=.85, saveresults=False, printerror=False,
                           printruntimes=False)
        runtimes_pagerank[i] = runtime
    print("Average Runtime PAGERANK: ", np.mean(runtimes_pagerank))
