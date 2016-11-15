from rdflib.plugins.parsers.ntriples import NTriplesParser, Sink
import os, pickle



# prepare DB
E2I = dict()
T2I = dict()
i=0 # sparse matrices are 1 based
j=0
k = 0 
class IndexSink(Sink):

	def triple(self,s,p,o):
		global i, j
		#parse s,p,o to dictionaries/databases
		s = s.toPython()
		p = p.toPython()
		o = o.toPython()
		try:
			tmp = E2I[s]
		except KeyError:
			E2I[s] = [i, 0]
			i += 1
		try:
			tmp = E2I[p]
		except KeyError:
			E2I[p] = [i, 0]
			i += 1
		try:
			tmp = E2I[o]
		except KeyError:
			E2I[o] = [i, 0]
			i += 1
		E2I[s][1] += 1
		E2I[p][1] += 1
		E2I[o][1] += 1
	
		
		try:
			tmp = T2I[tuple([s, p, o])]
		except KeyError:
			T2I[tuple([s, p, o])] = j
			j += 1
		if i%10000 == 0:
			print(i)
		

IndexSink = IndexSink()
parser = NTriplesParser(IndexSink)
with open("ekaw.nt", 'rb') as data:
	parser.parse(data)


print(len(E2I), len(T2I))

pickle.dump(E2I, open("e2i.pkl", "wb"))
pickle.dump(T2I, open("t2i.pkl", "wb"))


