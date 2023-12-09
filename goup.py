import os
import pandas as pd

# path
input_folder = '/home/share/shenglun/workspace/m1apre/HEK_predict'
output_folder = '/home/share/shenglun/workspace/m1apre/groupbydata'

# read data
input_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# for every csv
for input_file in input_files:
    # build path
    input_file_path = os.path.join(input_folder, input_file)

    # read data
    data = pd.read_csv(input_file_path)

    # go group by with first 3 columns combination ，calculate"Prediction" of 1 
    grouped_data = data.groupby([data.columns[1], data.columns[2], data.columns[3]])["Prediction"].mean()

    # DataFrame
    result_df = grouped_data.reset_index()

    # rename
    result_df.columns = ['chrom', 'chrom_pos', 'strand', '1_Percentage']

    output_file_path = os.path.join(output_folder, os.path.splitext(input_file)[0] + '_groupby.csv')

    # save
    result_df.to_csv(output_file_path, index=False)
