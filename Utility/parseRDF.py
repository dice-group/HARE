from rdflib.plugins.parsers.ntriples import NTriplesParser, Sink

import os, pickle
from Utility.config import data_dir

loadpath = data_dir + "KnowledgeBases/"
savepath = data_dir + "Matrices/"


def parseRDF(name):
    # prepare DB
    E2I = dict()
    T2I = dict()

    class IndexSink(Sink):
        i = 0
        j = 0

        def triple(self, s, p, o):

            # parse s,p,o to dictionaries/databases
            s = s.toPython()
            p = p.toPython()
            o = o.toPython()
            try:
                tmp = E2I[s]
            except KeyError:
                E2I[s] = [self.i, 0]
                self.i += 1
            try:
                tmp = E2I[p]
            except KeyError:
                E2I[p] = [self.i, 0]
                self.i += 1
            try:
                tmp = E2I[o]
            except KeyError:
                E2I[o] = [self.i, 0]
                self.i += 1
            E2I[s][1] += 1
            E2I[p][1] += 1
            E2I[o][1] += 1

            try:
                tmp = T2I[tuple([s, p, o])]
            except KeyError:
                T2I[tuple([s, p, o])] = self.j
                self.j += 1
            if self.j % 10000 == 0:
                print(self.j)

    IndexSink = IndexSink()
    parser = NTriplesParser(IndexSink)
    with open(loadpath + name, 'rb') as data:
        parser.parse(data)

    print("Distinct Entities: ", len(E2I))
    print("Distinct Triples: ", len(T2I))

    if ".ttl" in name:
        name = name[:-4]
    if ".nt" in name:
        name = name[:-3]
    pickle.dump(E2I, open(savepath + "e2i_" + name + ".pkl", "wb"))
    pickle.dump(T2I, open(savepath + "t2i_" + name + ".pkl", "wb"))
