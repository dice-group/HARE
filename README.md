# HARE
## Running HARE
First make sure you have installed `numpy, scipy, rdflib` (in their latest versions pip install --upgrade pip)

```
conda env create -f hare.yml
```
on linux: `conda activate hare`

on windows, mac: `source activate hare`

run experiment: `python experiment.py`

## Datasets
Please make sure to provide valid .nt or .ttl.
In the paper we used the following datasets:
  -Dbpedia (
  -Airports
  -LUBM
  -... 
We cleaned the datasets for syntactic errors (e.g. "4.5"xsd^^integer).
In case of DBPedia and LUBM please use `cat *.ttl > out.ttl´
