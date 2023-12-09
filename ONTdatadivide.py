import os
import csv
import pandas as pd

csv_folder = '/home/share/shenglun/workspace/m1apre/tmp_HEKfeature/tmp'
output_folder = '/home/share/shenglun/workspace/m1apre/data_HEK'
os.makedirs(output_folder, exist_ok=True)

def divide_by_motif(tmp_df):
    motifs = tmp_df['motif'].unique()
    for motif in motifs:
        tmp_motif = tmp_df[tmp_df['motif']==motif]
        print(tmp_motif)
        output_file_path = os.path.join(output_folder,f'{motif}.csv')
        tmp_motif.to_csv(output_file_path,mode = 'a')

for csv_file_name in os.listdir(csv_folder):
    if csv_file_name.endswith('.csv'):
        features = pd.read_csv(os.path.join(csv_folder, csv_file_name))
        features = features.rename(columns={'5':'motif'})
        divide_by_motif(features)


