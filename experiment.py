from Utility.getTransitionMatrices import getTransitionMatrices
from Utility.parseRDF import parseRDF
from Computations.hare import hare
from Computations.pagerank import pagerank
import numpy as np

repetitions = 5
data = "airports.nt" # "dbpedia_smaller.ttl"
print("WITH: ", data)
#parseRDF(data)
#getTransitionMatrices(data)

print(".....HARE.....")
runtimes_hare = np.array(repetitions*[.0])
for i in range(repetitions-1):
	runtime = hare(data, epsilon=10**(-2), damping = .85, saveresults=False, printerror=False, printruntimes=True)
	runtimes_hare[i] = runtime
print("Average Runtime HARE: ", np.mean(runtimes_hare))

#print(".....PAGERANK.....")
#runtimes_pagerank = np.array(repetitions*[.0])
#for i in range(repetitions):
#	runtime = pagerank(data, epsilon=10**(-3), damping = .85, saveresults=True, printerror=False, printruntimes=True)
#	runtimes_pagerank[i] = runtime
#print("Average Runtime PAGERANK: ", np.mean(runtimes_pagerank))
