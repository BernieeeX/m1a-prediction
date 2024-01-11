import os
import pandas as pd
import argparse

def filter_and_combine(input_dir_1, output_file_path):
    # 1. filter
    if not os.path.exists(input_dir_1):
        print(f"Input directory '{input_dir_1}' does not exist.")
        return

    # Check if there are CSV files in the input directory
    input_files = [f for f in os.listdir(input_dir_1) if f.endswith('.csv')]
    if not input_files:
        print(f"No CSV files found in the input directory '{input_dir_1}'.")
        return

    all_data = pd.DataFrame()

    for filename in input_files:
        input_path = os.path.join(input_dir_1, filename)
        df = pd.read_csv(input_path)
        filtered_df = df[df['1_Percentage'] != 0]
        motif_value = filename.split('.csv')[0]
        filtered_df['motif'] = motif_value
        filtered_df = filtered_df.drop(['1_Percentage'], axis=1)
        grouped_data = filtered_df.groupby(['chrom', 'chrom_pos', 'strand', 'motif']).agg({'Group_Count': 'sum', 'Count_of_1': 'sum'}).reset_index()
        all_data = pd.concat([all_data, grouped_data])

    final_grouped_data = all_data.groupby(['chrom', 'chrom_pos', 'strand', 'motif']).agg({'Group_Count': 'sum', 'Count_of_1': 'sum'}).reset_index()
    final_grouped_data.to_csv(output_file_path, index=False)

    # 2. processing
    df = pd.read_csv(output_file_path)
    df = df[df['chrom'] != '0']
    df.to_csv(output_file_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter and combine CSV files.")
    parser.add_argument("-i", "--input", help="Input directory containing CSV files", required=True)
    parser.add_argument("-o", "--output", help="Output file path for the final processed data", required=True)
    args = parser.parse_args()

    filter_and_combine(args.input, args.output)
