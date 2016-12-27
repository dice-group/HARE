from SPARQLWrapper import SPARQLWrapper, JSON
from Utility.config import data_dir

def getRankedLists(classes, method):
	savepath = data_dir + "RankedLists/" 
	if method == "HARE":
		loadpath = data_dir + "Results/" + "results_resources_dbpedia_HARE.txt"	
	if method == "PAGERANK":
		loadpath = data_dir + "Results/" + "results_dbpedia_PAGERANK.txt"
	


	for class_name in classes:
		    print(class_name)
		    query = """SELECT ?entity
		               WHERE {?entity a <http://dbpedia.org/ontology/""" + class_name + ">}"

		    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		    sparql.setQuery(query)
		    sparql.setReturnFormat(JSON)
		    results = sparql.query().convert()

		    entities = []
		    for result in results["results"]["bindings"]:
		        entities.append(result["entity"]['value'])

		    entities = set(entities)
		    with open(loadpath, "r") as f, open(savepath + class_name + "_" + method ".txt", "w+") as g:
		            for line in f:
		                    line = line.split(" ")
		                    if line[0] in entities:
		                            g.write(" ".join(line))


