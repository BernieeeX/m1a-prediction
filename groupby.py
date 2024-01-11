import os
import pandas as pd
import argparse

def groupby_and_save(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # read data
    input_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

    # for every csv
    for input_file in input_files:
        # build path
        input_file_path = os.path.join(input_folder, input_file)

        # read data
        data = pd.read_csv(input_file_path)

        # go group by with first 3 columns combination, calculate "Prediction" mean, count, and count of "1"
        grouped_data = data.groupby([data.columns[1], data.columns[2], data.columns[3]]).agg({
            "Prediction": ["mean", "count", lambda x: (x == 1).sum()]   # calculate mean, count, and count of "1"
        })

        # DataFrame
        result_df = grouped_data.reset_index()

        # rename
        result_df.columns = ['chrom', 'chrom_pos', 'strand', '1_Percentage', 'Group_Count', 'Count_of_1']

        output_file_path = os.path.join(output_folder, os.path.splitext(input_file)[0] + '_groupby.csv')

        # save
        result_df.to_csv(output_file_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Groupby data and calculate 'Prediction' mean, count, and count of '1'.")
    parser.add_argument("-i", "--input", help="Input folder containing CSV files", required=True)
    parser.add_argument("-o", "--output", help="Output folder for grouped data", required=True)
    args = parser.parse_args()

    groupby_and_save(args.input, args.output)
