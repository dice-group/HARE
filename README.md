# HARE
## Running HARE
```
conda env create -f hare.yml
```
on linux: `source activate hare`

on windows, mac: `source activate hare`

run experiment: `python experiment.py`

prepare the evaluation dataset: `python prepare_eval.py`

## Datasets
Please make sure to provide valid .nt or .ttl.



We cleaned the datasets for syntactic errors (e.g. "4.5"xsd^^integer).
In case of DBPedia and LUBM please use `cat *.ttl > out.ttl`
