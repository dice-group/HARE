from scipy import sparse as sparse
from scipy import io
import numpy as np
import pickle as pkl
import time
print("LOADING DICTIONARIES")
E2I = pkl.load(open("e2i.pkl", "rb"))
T2I = pkl.load(open("t2i.pkl", "rb"))
I2E = dict()
I2T = dict()
for key, val in E2I.items():
	I2E[val[0]] = key
for key, val in T2I.items():
	I2T[val] = key

tic = time.time()
print("LOADING F")
y = np.load("F.npz")
F = sparse.coo_matrix((y['data'],(y['row'],y['col'])),shape=y['shape'])

print("LOADING W")
y = np.load("W.npz")
W = sparse.coo_matrix((y['data'],(y['row'],y['col'])),shape=y['shape'])

print("CALCULATING P_N")
P = sparse.bmat([[None, W], [F, None]])
n = P.shape[0]

previous = np.ones(n)/n
ones = np.ones(n)

error = 1
epsilon = 10**(-3)
damping = 0.85

iterationcounter = 0 
while error > epsilon:
	tmp = np.array(previous)
	if iterationcounter%2 == 0:
		previous = damping*P.T.dot(previous) + (1-damping)*ones
	else:
		previous = P.T.dot(previous)
	error = np.linalg.norm(tmp - previous)	
	print(error)
tac = time.time()
print("RUNTIME", tac-tic)

print("WRITING RESULTS")
with open("results_resources.txt", "w") as results:
	for i, x in sorted(enumerate(previous), key = lambda x: -x[1]):
		tmp = ""
		if i < len(I2T):		
			tmp += str(I2T[i])
			results.write(tmp +  " " + str(x) + "\n")
		else:
			tmp += str(I2E[i- len(I2T)])
			results.write(tmp + " " + str(x) + "\n")


