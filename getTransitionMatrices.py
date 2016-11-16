import pickle as pkl
import gc
import numpy as np
from scipy import sparse as sparse
from scipy import io
from collections import defaultdict

E2I = pkl.load(open("e2i.pkl", "rb"))
T2I = pkl.load(open("t2i.pkl", "rb"))
i = 0
F = sparse.dok_matrix((len(E2I), len(T2I)))
W = sparse.dok_matrix((len(T2I), len(E2I)))
f = defaultdict(int)
w = defaultdict(int)
print("CONSTRUCTING DICTIONARY OF KEYS")

k = 0
for t, i in T2I.items():
	k += 1
	if k%1000 == 0:
		print(str(k/len(T2I)) + "%")
	for e in t:		
		#edge from entity_j to triple_i detected
		j = E2I[e][0]
		w[(i, j)] = 1/3
		f[(j, i)] = 1/E2I[e][1]
print("UPDATING MATRIX F...")
for key, val in f.items():
	F[key] = val
print("UPDATING MATRIX W...")
for key, val in w.items():
	W[key] = val
print("DELETING DICTIONARY...")
del f
del w
gc.collect()
del gc.garbage[:]
print("SAVING MATRIX F...")
f_coo=F.tocoo()
row=f_coo.row
col=f_coo.col
data=f_coo.data
shape=f_coo.shape
np.savez("F",row=row,col=col,data=data,shape=shape)
print("SAVING MATRIX W...")
w_coo=W.tocoo()
row=w_coo.row
col=w_coo.col
data=w_coo.data
shape=w_coo.shape
np.savez("W",row=row,col=col,data=data,shape=shape)
