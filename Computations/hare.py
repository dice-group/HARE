from scipy import sparse as sparse
from scipy import io
import numpy as np
import pickle as pkl
import time

from Utility.config import data_dir

load_dir = data_dir + "Matrices/"
save_dir = data_dir + "Results/"


def hare(name, epsilon, damping, saveresults=True, printerror=False, printruntimes=False):
    if ".ttl" in name: name = name[:-4]
    if ".nt" in name: name = name[:-3]
    E2I = pkl.load(open(load_dir + "e2i_" + name + ".pkl", "rb"))
    T2I = pkl.load(open(load_dir + "t2i_" + name + ".pkl", "rb"))
    tic = time.time()
    print("(Parallel) LOADING F")
    y = np.load(load_dir + "F_" + name + ".npz")
    F = sparse.coo_matrix((y['data'], (y['row'], y['col'])), shape=y['shape'])

    print("(Parallel) LOADING W")
    y = np.load(load_dir + "W_" + name + ".npz")
    W = sparse.coo_matrix((y['data'], (y['row'], y['col'])), shape=y['shape'])

    print("(Parallel) CALCULATING P_N")
    P = sparse.csr_matrix(F.dot(W))
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
        if printerror:
            print(error)

    alpha = len(E2I)
    beta = len(T2I)
    factor1 = alpha/(alpha+beta)
    factor2 = beta/(alpha+beta)
    tripledistribution1 = F.T.dot(previous)
    resourcedistribution = factor1 * previous
    tripledistribution = factor2*tripledistribution1

    print ("(Parallel) FINAL vector ", np.concatenate((tripledistribution, resourcedistribution)))
    tac = time.time()
    runtime2 = tac - tic2
    if printruntimes:
        print("(Parallel) LOAD TIME: ", runtime)
        print("(Parallel) RUNTIME without load: ", runtime2)
    if saveresults:
        print("(Parallel) LOADING DICTIONARIES")
        I2E = dict()
        I2T = dict()
        for key, val in E2I.items():
            I2E[val[0]] = key
        for key, val in T2I.items():
            I2T[val] = key

        print("(Parallel) WRITING RESULTS")
        with open(save_dir + "results_resources_" + name + "_HARE.txt", "w") as results:
            for i, x in sorted(enumerate(resourcedistribution), key=lambda x: -x[1]):
                tmp = ""
                tmp += str(I2E[i])
                results.write(tmp + " " + str(x) + "\n")

        with open(save_dir + "results_triples_" + name + "_HARE.txt", "w") as results:
            for i, x in sorted(enumerate(tripledistribution), key=lambda x: -x[1]):
                tmp = ""
                for n in I2T[i]:
                    tmp += str(n) + " "
                results.write(tmp + " " + str(x) + "\n")
    return runtime2
