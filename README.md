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

**(1). Fast5 files convertion**

The multi_read format obtained from ONT sequencing needs to be converted into smaller-sized fast5 files using a tool before proceeding with the next steps.

```
multi_to_single_fast5 -i /path/to/multi_fast5 -s /path/to/single_fast5 -t 12 --recursive 
```

**(2). Basecalling by using guppy**

```
guppy_basecaller -i /path/to/single_fast5 -s /path/to/fastq --flowcell FLO-MIN106 --kit SQK-RNA002 --recursive --fast5_out --cpu_threads_per_caller 5
```

**(3). Re-squiggle the raw signals**

Tombo resquiggle reanalyzes these signals, attempting to correct or improve any errors that may have occurred previously, thereby enhancing the accuracy and reliability of the data. Using the referance gene fasta file to do the re-squiggle

```
tombo resquiggle --overwrite /path/to/fastq/workspace /path/to/referance_gene_fasta.fa --processes 5 --fit-global-scale --corrected-group RawGenomeCorrected_000 --include-event-stdev --num-most-common-errors 5
```

**(3). Feature extraction**

Utilizing ``feature_extraction.py`` to extract electrical characteristics (such as signal means, standard deviations, and lengths) from re-squiggled events. Within each read, we identify NNANN motifs along the sequence and capture pertinent features for each position (-2, -1, 0, 1, 2) within the 5-mer.

```
python feature_extraction.py -i /path/to/fastq/workspace -o /path/to/feature_directory -t 12
```

# **Ⅲ. Using pre-processed data for result prediction or model training**

**(1). m1a-prediction**

Predicting N1-Methyladenosine by using our trained model.

```
python predict_xgboost.py -i /path/to/input_folder -o /path/to/output_folder -m /path/to/model_folder
```

**(2). Other modification-prediction-model training**

If users want to train their own model for RNA modifications of interest, they can replicate the pre-processing steps by processing the raw data to obtain two sets of feature data: negative and positive. Then, they can use our script to train their own model. The script we provide will generate a model ensemble consisting of 256 models, along with evaluation metrics for all models, including accuracy, F1 score, MCC, AUPR, and AUROC, as well as ROC curves.

```
python training.py -m /path/to/mod_folder -u /path/to/unmod_folder -o /path/to/output_dir -e /path/to/evaluation_dir -p /path/to/plot_folder
```

# **Ⅳ. Site level analysis**

After obtaining prediction results at the reads level using machine learning, we will provide a script to map the reads-level results to the site level.

**(1). Classification processing of prediction result**

 Using the provided script to categorize the predicted results according to motifs.

 ```
python process_csv.py -i /path/to/prediction_result_folder -o /path/to/output_folder
 ```

Perform a groupby operation on the classified data.

 ```
python groupby.py -i /path/to/processed_csv -o /path/to/output_folder
 ```

Integrate group-by results

 ```
python filter_and_combine.py -i /path/to/group-by_directory -o /path/to/output_file.csv
 ```

**(2). Binomil test**

Users can select the parameters for the binomial distribution test based on the features of the test data themselves. the default p = 0.4, a = 0.01.

 ```
python binomial.py -i /path/to/input_directory -o /path/to/output_directory -p 0.4 -a 0.01
 ```



All suggestions are welcome to Yuxin.Zhang17@student.xjtlu.edu.cn or Shenglun.Chen22@student.xjtlu.edu.cn


