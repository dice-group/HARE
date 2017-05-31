from Utility.getRankedLists import getRankedLists
from Utility.prepareEval import prepareEval

methods = ["HARE"]

classes = ["City", "University", "VideoGame", "SpaceStation", "Mountain", "Hotel",
	            "EurovisionSongContestEntry", "Drug", "Comedian", "ChessPlayer",
	            "Band", "Album", "Person", "Automobile", "HistoricPlace", "Town",	
	            "MilitaryConflict", "ProgrammingLanguage", "Country"]

for method in methods:
	getRankedLists(classes, method)
	prepareEval(classes, method)
