# HARE
## Running HARE
We use the anaconda package. To make sure that you have all the required packages, install anaconda and do
```
conda env create -f hare.yml
source activate hare
```
To run an experiment use `python experiment.py`

To change the dataset please save your .ttl or .nt file in HARE/Data/KnowledgeBases and edit line 8 in "experiment.py"

To save the results please change the "saveresults" parameter in the hare and pagerank function to "true".

To prepare the evaluation dataset, please download the required DBpedia knowledge bases and run the experiment on them with "saveresults = true", afterwards do `python eval.py`. The .tsv for evaluation and comparison are saved in this directory.

## Datasets
Please make sure to provide valid .nt or .ttl.

We cleaned the datasets for syntactic errors (e.g. "4.5"xsd^^integer).
In case of DBpedia and LUBM please combine several files into one using `cat *.ttl > out.ttl`
