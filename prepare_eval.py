from Utility.getRankedLists import getRankedLists
from Utility.prepareEval import prepareEval

method = "HARE" #PAGERANK

classes = ["City", "University", "VideoGame", "SpaceStation", "Mountain", "Hotel",
	            "EurovisionSongContestEntry", "Drug", "Comedian", "ChessPlayer",
	            "Band", "Album", "Person", "Automobile", "HistoricPlace", "Town",	
	            "MilitaryConflict", "ProgrammingLanguage", "Country"]

getRankedLists(classes, method)
preparesEval(classes, method)
