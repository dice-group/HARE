from Utility.getTransitionMatrices import getTransitionMatrices
from Utility.parseRDF import parseRDF
from Computations.hare import hare
parseRDF("example.ttl")
getTransitionMatrices("example.ttl")
hare("example.ttl", epsilon=10**(-3), damping = .85, saveresults=True, printerror=False)
