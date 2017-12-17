from scipy import sparse as sparse
from scipy import io
import numpy as np
import pickle as pkl
import time
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import RDF
import re

from Utility.config import data_dir

load_dir = data_dir + "Matrices/"
save_dir = data_dir + "Results/"
loadpath = data_dir + "KnowledgeBases/"


def hare(name, epsilon, damping, saveresults = True, printerror = False, printruntimes = False):
    g = Graph()
    hareprop = URIRef("http://aksw.org/property/hareRank")
    if ".ttl" in name:
        g.parse(loadpath + name, format="n3")
        print (name)
        name = name[:-4]
    if ".nt" in name:
        g.parse(loadpath + name, format="nt")
        name = name[:-3]
    tic = time.time()
    print("LOADING F")
    y = np.load(load_dir + "F_" + name + ".npz")
    F = sparse.coo_matrix((y['data'], (y['row'], y['col'])), shape=y['shape'])

    print("LOADING W")
    y = np.load(load_dir + "W_" + name + ".npz")
    W = sparse.coo_matrix((y['data'], (y['row'], y['col'])), shape=y['shape'])

    print("CALCULATING P_N")
    P = sparse.csr_matrix(F.dot(W))
    n = P.shape[0]

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

    resourcedistribution = previous
    tripledistribution = F.T.dot(previous)
    tac = time.time()
    runtime = tac - tic
    runtime2 = tac - tic2
    if (printruntimes):
        print("RUNTIME with load: ", runtime)
        print("RUNTIME without load: ", runtime2)
    if (saveresults):
        print("LOADING DICTIONARIES")
        E2I = pkl.load(open(load_dir + "e2i_" + name + ".pkl", "rb"))
        T2I = pkl.load(open(load_dir + "t2i_" + name + ".pkl", "rb"))
        I2E = dict()
        I2T = dict()
        for key, val in E2I.items():
            I2E[val[0]] = key
        for key, val in T2I.items():
            I2T[val] = key

        print("WRITING RESULTS")
        for i, x in sorted(enumerate(resourcedistribution), key=lambda x: -x[1]):
            if not "http://" in str(I2E[i]):
                temp = re.sub(r'\W+', '', str(I2E[i]))
                g.add((URIRef(temp), hareprop, Literal(str(x))))
        for i, x in sorted(enumerate(tripledistribution), key=lambda x: -x[1]):
            statementId = BNode()
            g.add((statementId, RDF.type, RDF.Statement))
            tmp = ""
            for n in I2T[i]:
                tmp += str(n) + " "
            triple = tmp.split(" ")
            g.add((statementId, RDF.subject, URIRef(triple[0])))
            g.add((statementId, RDF.predicate, URIRef(triple[1])))

            if "http://" in str(triple[2]):
             g.add((statementId, RDF.object, URIRef(triple[2])))
            else:
             g.add((statementId, RDF.object, Literal(triple[2])))

            g.add((statementId, hareprop, Literal(str(x))))

        g.serialize(save_dir + "dataset_" + name + "_HARE.ttl", format='turtle')
    return runtime2
