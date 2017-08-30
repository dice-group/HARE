from scipy import sparse as sparse
from scipy import io
import numpy as np
import pickle as pkl
import time

from Utility.config import data_dir

#load_dir = data_dir + "Matrices/"
save_dir = data_dir + "Results_dense/"
def hare(name, epsilon, damping, saveresults=True, printerror=False, printruntimes=False):
#	if ".ttl" in name: name = name[:-4]
#	if ".nt" in name: name = name[:-3]

	tic = time.time()
#	print("LOADING F")
	y = np.load(name + "/F.npz")
	F = sparse.coo_matrix((y['data'],(y['row'],y['col'])),shape=y['shape']).todense()

#	print("LOADING W")
	y = np.load(name + "/W.npz")
	W = sparse.coo_matrix((y['data'],(y['row'],y['col'])),shape=y['shape']).todense()

#	print("CALCULATING P_N")
	P = np.dot(F,W)
	n = P.shape[0]

	previous = np.ones(n)/n
	ones = np.ones(n)/n

	error = 1
	tic2 = time.time()
	
	while error > epsilon:
		tmp = np.array(previous)
		previous = damping*np.dot(P.T,previous.T) + (1-damping)*ones
		error = np.linalg.norm(tmp - previous)
		if(printerror):
			print(error)

	resourcedistribution = previous
	tac = time.time()
	tripledistribution = np.dot(F.T,previous)	
	runtime = tac-tic
	runtime2 = tac-tic2
	if(printruntimes):
		print("RUNTIME with load: ", runtime)
		print("RUNTIME without load: ", runtime2)
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
	return runtime2
