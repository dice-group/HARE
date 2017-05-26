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

	tic = time.time()
	print("LOADING F")
	y = np.load(load_dir + "F_" + name + ".npz")
	F = sparse.coo_matrix((y['data'],(y['row'],y['col'])),shape=y['shape'])

	print("LOADING W")
	y = np.load(load_dir + "W_" + name + ".npz")
	W = sparse.coo_matrix((y['data'],(y['row'],y['col'])),shape=y['shape'])

	print("CALCULATING P_N")
	P = sparse.csr_matrix(F.dot(W))
	n = P.shape[0]

	previous = np.ones(n)/n
	ones = np.ones(n)/n

	error = 1

	while error > epsilon:
		tmp = np.array(previous)
		previous = damping*P.T.dot(previous) + (1-damping)*ones
		error = np.linalg.norm(tmp - previous)
		if(printerror):
			print(error)

	resourcedistribution = previous
	tripledistribution = F.T.dot(previous)
	tac = time.time()
	runtime = tac-tic
	if(printruntimes):
		print("RUNTIME: ", runtime)
	if(saveresults):
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
		with open(save_dir + "results_resources_" + name + "_HARE.txt", "w") as results:
			for i, x in sorted(enumerate(resourcedistribution), key = lambda x: -x[1]):
				tmp = ""		
				tmp += str(I2E[i])
				results.write(tmp +  " " + str(x) + "\n")

		with open(save_dir + "results_triples_" + name + "_HARE.txt", "w") as results:
			for i, x in sorted(enumerate(tripledistribution), key = lambda x: -x[1]):
				tmp = ""		
				for n in I2T[i]:
					tmp += str(n) + " "
				results.write(tmp +  " " + str(x) + "\n")
	return runtime
