import pickle as pkl
import numpy as np
import sys
from scipy import sparse as sparse
from scipy import io
from collections import defaultdict
from Utility.config import data_dir

def getTransitionMatrices(name):
	loadpath = data_dir + "Matrices/"
	savepath = data_dir + "Matrices/"
	if ".ttl" in name: name = name[:-4]
	if ".nt" in name: name = name[:-3]	
	E2I = pkl.load(open(loadpath + "e2i_" + name + ".pkl", "rb"))
	T2I = pkl.load(open(loadpath + "t2i_" + name + ".pkl", "rb"))
	i = 0
	F = sparse.dok_matrix((len(E2I), len(T2I)))
	W = sparse.dok_matrix((len(T2I), len(E2I)))
	f = defaultdict(int)
	w = defaultdict(int)
	print("CONSTRUCTING DICTIONARY OF KEYS")

	k = 0
	for t, i in T2I.items():
		k += 1
		sys.stdout.write('\r')
		sys.stdout.write("[%-20s] %d%%" % ('='*int(k/len(T2I)*20), 100*k/len(T2I)))
		for e in t:		
			#edge from entity_j to triple_i detected
			j = E2I[e][0]
			w[(i, j)] = 1/3
			f[(j, i)] = 1/E2I[e][1]
	print("\nUPDATING MATRIX F...")
	k = 0 
	for key, val in f.items():
		k+=1
		sys.stdout.write('\r')
		sys.stdout.write("[%-20s] %d%%" % ('='*int(k/len(f)*20), 100*k/len(f)))
		F[key] = val
	print("\nUPDATING MATRIX W...")
	k = 0
	for key, val in w.items():
		k+=1
		sys.stdout.write("\r[%-20s] %d%%" % ('='*int(k/len(w)*20), 100*k/len(w)))
		W[key] = val
	print("\nSAVING MATRIX F...")
	f_coo=F.tocoo()
	row=f_coo.row
	col=f_coo.col
	data=f_coo.data
	shape=f_coo.shape
	np.savez(savepath + "F_" + name,row=row,col=col,data=data,shape=shape)
	print("SAVING MATRIX W...")
	w_coo=W.tocoo()
	row=w_coo.row
	col=w_coo.col
	data=w_coo.data
	shape=w_coo.shape
	np.savez(savepath + "W_" + name,row=row,col=col,data=data,shape=shape)
