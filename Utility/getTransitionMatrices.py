import pickle as pkl
import numpy as np
import sys
from scipy import sparse as sparse

from collections import defaultdict
from multiprocessing import Pool
from Utility.config import data_dir

def fillFMatrix(f , entitytoindex, tripletoindex, savepath, name):
    F = sparse.dok_matrix((len(entitytoindex), len(tripletoindex)))
    print("\nUPDATING MATRIX F...")
    k = 0
    for key, val in f.items():
        k += 1
        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%%" % ('=' * int(k / len(f) * 20), 100 * k / len(f)))
        F[key] = val
    print("\nSAVING MATRIX F...")
    f_coo = F.tocoo()
    row = f_coo.row
    col = f_coo.col
    data = f_coo.data
    shape = f_coo.shape
    np.savez(savepath + "F_" + name, row=row, col=col, data=data, shape=shape)



def fillWMatrix(w,entitytoindex,tripletoindex,savepath,name):
    W = sparse.dok_matrix([len(tripletoindex), len(entitytoindex)])
    print("\nUPDATING MATRIX W...")
    k = 0
    for key, val in w.items():
        k += 1
        sys.stdout.write("\r[%-20s] %d%%" % ('=' * int(k / len(w) * 20), 100 * k / len(w)))
        W[key] = val

    print("SAVING MATRIX W...")
    w_coo = W.tocoo()
    row = w_coo.row
    col = w_coo.col
    data = w_coo.data
    shape = w_coo.shape
    np.savez(savepath + "W_" + name, row=row, col=col, data=data, shape=shape)

def getTransitionMatrices(name):
    loadpath = data_dir + "Matrices/"
    savepath = data_dir + "Matrices/"
    if ".ttl" in name: name = name[:-4]
    if ".nt" in name: name = name[:-3]
    entitytoindex = pkl.load(open(loadpath + "e2i_" + name + ".pkl", "rb"))
    tripletoindex = pkl.load(open(loadpath + "t2i_" + name + ".pkl", "rb"))
    i = 0
    f = defaultdict(int)
    w = defaultdict(int)
    print("CONSTRUCTING DICTIONARY OF KEYS")
    k = 0
    for t, i in tripletoindex.items():
        k += 1
        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%%" % ('=' * int(k / len(tripletoindex) * 20), 100 * k / len(tripletoindex)))
        for e in t:
            # edge from entity_j to triple_i detected
            j = entitytoindex[e][0]
            w[(i, j)] = 1 / 3
            f[(j, i)] = 1 / entitytoindex[e][1]

    pool = Pool(2)
    pool.apply_async(fillFMatrix, (f, entitytoindex, tripletoindex, savepath, name))
    pool.apply_async(fillFMatrix, (f, entitytoindex, tripletoindex, savepath, name))


