from scipy import sparse as sparse
from scipy import io
import numpy as np
import pickle as pkl
import time

from Utility.config import data_dir

load_dir = data_dir + "Matrices/"
save_dir = data_dir + "Results/"


def pagerank(name, epsilon, damping, saveresults = True, printerror = False, printruntimes = False):
    if ".ttl" in name: name = name[:-4]
    if ".nt" in name: name = name[:-3]

    tic = time.time()
    print("(Parallel) LOADING F")
    y = np.load(load_dir + "F_" + name + ".npz")
    F = sparse.coo_matrix((y['data'], (y['row'], y['col'])), shape=y['shape'])

    print(" (Parallel) LOADING W")
    y = np.load(load_dir + "W_" + name + ".npz")
    W = sparse.coo_matrix((y['data'], (y['row'], y['col'])), shape=y['shape'])

    print("(Parallel) CALCULATING P_N")
    P = sparse.bmat([[None, W], [F, None]])
    n = P.shape[0]
    tac1 = time.time()
    runtime = tac1 - tic
    previous = np.ones(n) / n
    ones = np.ones(n) / n

    error = 1
    tic2 = time.time()
    while error > epsilon:
        tmp = np.array(previous)
        previous = damping * P.T.dot(previous) + (1 - damping) * ones
        error = np.linalg.norm(tmp - previous)
        if (printerror):
            print(error)

    distribution = previous
    tac = time.time()

    runtime2 = tac - tic2
    if printruntimes:
        print("(Parallel) LOAD TIME: ", runtime)
        print("(Parallel) RUNTIME without load: ", runtime2)
    if saveresults:
        print("(Parallel) LOADING DICTIONARIES")
        entitytoindex = pkl.load(open(load_dir + "e2i_" + name + ".pkl", "rb"))
        tripletoindex = pkl.load(open(load_dir + "t2i_" + name + ".pkl", "rb"))
        indextoentity = dict()
        indextotriple = dict()
        for key, val in entitytoindex.items():
            indextoentity[val[0]] = key
        for key, val in tripletoindex.items():
            indextotriple[val] = key

        print("(Parallel) WRITING RESULTS")
        with open(save_dir + "results_" + name + "_PAGERANK.txt", "w") as results:
            for i, x in sorted(enumerate(previous), key=lambda x: -x[1]):
                tmp = ""
                if i < len(indextotriple):
                    tmp += str(indextotriple[i])
                    results.write(tmp + " " + str(x) + "\n")
                else:
                    tmp += str(indextoentity[i - len(indextotriple)])
                    results.write(tmp + " " + str(x) + "\n")
    return runtime
