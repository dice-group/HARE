# HARE
## Running HARE
```
conda env create -f hare.yml
```
on linux: `source activate hare`

on windows, mac: `source activate hare`

run experiment: `python experiment.py`
to change the dataset please save your .ttl or .nt file in HARE/Data/KnowledgeBases and edit line 8 in "experiment.py"
to save the results please change the "saveresults" parameter in the hare and pagerank function to "true".

to prepare the evaluation dataset, please download the required dbpedia knowledgebases and run the experiment on them with "saveresults = true", afterwards do `python eval.py` the .tsv for evaluation and comparison are saved in this directory.
## Datasets
Please make sure to provide valid .nt or .ttl.



We cleaned the datasets for syntactic errors (e.g. "4.5"xsd^^integer).
In case of DBPedia and LUBM please use `cat *.ttl > out.ttl`
