from Utility.getTransitionMatrices import getTransitionMatrices
from Utility.parseRDF import parseRDF
from Computations.hare import hare
parseRDF("example.ttl")
getTransitionMatrices("example.ttl")
hare("example.ttl", saveresults=False, printerror=False)
