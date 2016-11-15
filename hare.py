from scipy import sparse as sparse
from scipy import io
import numpy as np
import pickle as pkl
E2I = pkl.load(open("e2i.pkl", "rb"))
T2I = pkl.load(open("t2i.pkl", "rb"))
I2E = dict()
I2T = dict()
for key, val in E2I.items():
	I2E[val[0]] = key
for key, val in T2I.items():
	I2T[val] = key


y = np.load("F.npz")
F = sparse.coo_matrix((y['data'],(y['row'],y['col'])),shape=y['shape'])

y = np.load("W.npz")
W = sparse.coo_matrix((y['data'],(y['row'],y['col'])),shape=y['shape'])

P = sparse.csr_matrix(F.dot(W))
n = P.shape[0]

previous = np.ones(n)/n
ones = np.ones(n)

error = 1
epsilon = 10**(-3)
damping = 0.85

print(P.todense())
while error > epsilon:
	tmp = np.array(previous)
	previous = damping*P.T.dot(previous) + (1-damping)*ones
	error = np.linalg.norm(tmp - previous)	
	print(error)

with open("results_resources.txt", "w") as results:
	for i, x in sorted(enumerate(previous), key = lambda x: -x[1]):
		tmp = ""		
		tmp += str(I2E[i])
		results.write(tmp +  " " + str(x) + "\n")

tripledistribution = F.T.dot(previous)
with open("results_triples.txt", "w") as results:
	for i, x in sorted(enumerate(tripledistribution), key = lambda x: -x[1]):
		tmp = ""		
		for n in I2T[i]:
			tmp += str(n) + " "
		results.write(tmp +  " " + str(x) + "\n")
