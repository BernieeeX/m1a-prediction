**m1A-prediction**

**Quantitative profiling N1-Methyladenosine (m1A) RNA methylation from Oxford Nanopore direct RNA sequencing data**

**The default models are applicable only to ONT sequencing data**

# **Ⅰ. Model Download and dependence installation**

(1). Model Download

  Users can directly use the following commands to download the models：
```
wget https://github.com/BernieeeX/m1a-prediction/tree/main/models

```
(2). Dependence installation

  The ``ont_fast5_api`` is a Python API for handling Fast5 files from Oxford Nanopore Technologies (ONT). 
  
  Source code: https://github.com/nanoporetech/ont_fast5_api
  
  it is available on github where it can be built from source:

    git clone https://github.com/nanoporetech/ont_fast5_api
    pip install ./ont_fast5_api

  The ``pyguppyclient``  is a Python client library for communicating with the Guppy server from Oxford Nanopore Technologies (ONT). The Guppy server from ONT is a server-side software used for analyzing genetic sequencing data, capable of receiving raw electrical signal data and converting it into DNA sequences.

  Source code: https://github.com/nanoporetech/pyguppyclient
  
    pip install pyguppyclient

  Dependence list:


**Source code dependence**

soft or module | version
---|---
bedtools | v2.29.2
samtools | 1.3.1
minimap2 | 2.17-r941
python                               |3.7.3
h5py                               |2.9.0
statsmodels                        |0.10.0
joblib                        |0.16.0
xgboost                       |0.80
pysam                         |0.16.0.1
tqdm                          |4.39.0
pycairo                       |1.19.1
scikit-learn              |0.22

  
# **Ⅱ. Pre-processing**






# m1a-prediction
#Part 1 model training
#Get the fast5 file of IVT
#multi_to_single_fast5
multi_to_single_fast5 -i /home/share/shenglun/workspace/m1apre/preprocess/IVT_normalA_fast5 -s /home/share/shenglun/workspace/m1apre/preprocess/A_single_fast5
multi_to_single_fast5 -i /home/share/shenglun/workspace/m1apre/preprocess/IVT_m1A_fast5 -s /home/share/shenglun/workspace/m1apre/preprocess/m1a_single_fast5

# guppy basecalling
guppy_basecaller -i /home/share/shenglun/workspace/m1apre/preprocess/A_single_fast5 -s /home/share/shenglun/workspace/m1apre/preprocess/A_fastq --flowcell FLO-MIN106 --kit SQK-RNA002 --recursive --fast5_out --cpu_threads_per_caller 5
guppy_basecaller -i /home/share/shenglun/workspace/m1apre/preprocess/m1a_single_fast5 -s /home/share/shenglun/workspace/m1apre/preprocess/m1a_fastq --flowcell FLO-MIN106 --kit SQK-RNA002 --recursive --fast5_out --cpu_threads_per_caller 5

# Tombo resquiggle
tombo resquiggle --overwrite /home/share/shenglun/workspace/m1apre/preprocess/m1a_fastq/workspace /home/share/shenglun/workspace/m1apre/preprocess/ref.fa --processes 5 --fit-global-scale --corrected-group RawGenomeCorrected_000 --include-event-stdev --num-most-common-errors 5 
tombo resquiggle --overwrite /home/share/shenglun/workspace/m1apre/preprocess/A_fastq/workspace /home/share/shenglun/workspace/m1apre/preprocess/ref.fa --processes 5 --fit-global-scale --corrected-group RawGenomeCorrected_000 --include-event-stdev --num-most-common-errors 5 

# Feature extraction
python feature_extraction.py -i /home/share/shenglun/workspace/m1apre/preprocess/A_fastq/workspace -o /home/share/shenglun/workspace/m1apre/Afeature -t 12
python feature_extraction.py -i /home/share/shenglun/workspace/m1apre/preprocess/m1a_fastq/workspace -o /home/share/shenglun/workspace/m1apre/m1afeature -t 8

# Training or Predicting
python predict_xgboost.py -i /path/to/input_folder -o /path/to/output_folder -m /path/to/model_folder
python training.py -m /path/to/mod_folder -u /path/to/unmod_folder -o /path/to/output_dir -e /path/to/evaluation_dir -p /path/to/plot_folder

# Process predict result
python groupby.py -i /path/to/input_folder -o /path/to/output_folder
python filter_and_combine.py -i /path/to/input_directory -o /path/to/output_file.csv

# Binomil test
python binomial.py -i /path/to/input_directory -o /path/to/output_directory -p 0.4 -a 0.01


### Additional csv file processing script
python process_csv.py -i /path/to/input_folder -o /path/to/output_folder
