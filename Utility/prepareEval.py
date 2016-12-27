from SPARQLWrapper import SPARQLWrapper, JSON
import random
def haslabel(ent):
	query = """
		SELECT ?label
		WHERE {<""" + ent + """> rdfs:label ?label . 
		FILTER (lang(?label)="en") }
	"""
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	labels = []
	for result in results["results"]["bindings"]:
		labels.append(result["label"]['value'])
	return labels



classes = ["Disease", "City", "University", "VideoGame", "SpaceStation", "Mountain", "Hotel",
                "EurovisionSongContestEntry", "Drug", "Comedian", "ChessPlayer",
                "Band", "Album", "Person", "Automobile", "HistoricPlace", "Town",
                "MilitaryConflict", "ProgrammingLanguage", "Country"]

with open("eval.tsv", "w") as evaltsv, open("compare.tsv", "w") as comparetsv:

	for c in classes:
		evaltsv.write(c + 2*'\n')
		comparetsv.write(c + 2*'\n')
		rankedList = []
		with open(c + ".txt", "r") as classrankings:
			for classranking in classrankings:
				entity, ranking = classranking.split(" ")
				rankedList.append(entity)
		evaltop = []
		for ent in rankedList:
			label = haslabel(ent)
			if label:
				evaltop.append(label[0])
			if len(evaltop) > 4:
				break
			evalbot = []
		for ent in reversed(rankedList):
			label = haslabel(ent)
			if label:
				evalbot.append(label[0])
			if len(evalbot) > 4:
				break	
		evallist = evaltop + list(reversed(evalbot))
		for ent in evallist:
			print(ent)
			comparetsv.write(ent + '\n')
		comparetsv.write('\n')
		random.shuffle(evallist)
		for ent in evallist:
			evaltsv.write(ent + '\n')
		evaltsv.write('\n')
