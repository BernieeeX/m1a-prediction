# m6a-prediction
#Part 1 model training
#Get the fast5 file of IVT
#multi_to_single_fast5
multi_to_single_fast5 -i /home/share/shenglun/workspace/m1apre/preprocess/IVT_normalA_fast5 -s /home/share/shenglun/workspace/m1apre/preprocess/A_single_fast5
multi_to_single_fast5 -i /home/share/shenglun/workspace/m1apre/preprocess/IVT_m1A_fast5 -s /home/share/shenglun/workspace/m1apre/preprocess/m1a_single_fast5

# guppy basecalling
guppy_basecaller -i /home/share/shenglun/workspace/m1apre/preprocess/A_single_fast5 -s /home/share/shenglun/workspace/m1apre/preprocess/A_fastq --flowcell FLO-MIN106 --kit SQK-RNA002 --recursive --fast5_out --cpu_threads_per_caller 5
guppy_basecaller -i /home/share/shenglun/workspace/m1apre/preprocess/m1a_single_fast5 -s /home/share/shenglun/workspace/m1apre/preprocess/m1a_fastq --flowcell FLO-MIN106 --kit SQK-RNA002 --recursive --fast5_out --cpu_threads_per_caller 5

#tombo resquiggle
tombo resquiggle --overwrite /home/share/shenglun/workspace/m1apre/preprocess/m1a_fastq/workspace /home/share/shenglun/workspace/m1apre/preprocess/ref.fa --processes 5 --fit-global-scale --corrected-group RawGenomeCorrected_000 --include-event-stdev --num-most-common-errors 5 
tombo resquiggle --overwrite /home/share/shenglun/workspace/m1apre/preprocess/A_fastq/workspace /home/share/shenglun/workspace/m1apre/preprocess/ref.fa --processes 5 --fit-global-scale --corrected-group RawGenomeCorrected_000 --include-event-stdev --num-most-common-errors 5 

#feature extraction
python feature_extraction.py -i /home/share/shenglun/workspace/m1apre/preprocess/A_fastq/workspace -o /home/share/shenglun/workspace/m1apre/Afeature -t 12
python feature_extraction.py -i /home/share/shenglun/workspace/m1apre/preprocess/m1a_fastq/workspace -o /home/share/shenglun/workspace/m1apre/m1afeature -t 8
