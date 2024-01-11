import os
import pandas as pd
from scipy.stats import binom_test
import argparse

def binomial_test_filter(input_dir, output_dir, p_expected, alpha):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            input_path = os.path.join(input_dir, filename)

            df = pd.read_csv(input_path)

            df['P_Value'] = df.apply(lambda row: binom_test(row['Count_of_1'], n=row['Group_Count'], p=p_expected, alternative='greater'), axis=1)

            significant_df = df[df['P_Value'] < alpha]

            output_filename = os.path.join(output_dir, filename)

            significant_df.to_csv(output_filename, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply binomial test filter to CSV files.")
    parser.add_argument("-i", "--input", help="Input directory containing CSV files", required=True)
    parser.add_argument("-o", "--output", help="Output directory for filtered results", required=True)
    parser.add_argument("-p", "--p_expected", type=float, default=0.4, help="Expected probability for binomial test")
    parser.add_argument("-a", "--alpha", type=float, default=0.01, help="Significance level (alpha) for binomial test")
    args = parser.parse_args()

    binomial_test_filter(args.input, args.output, args.p_expected, args.alpha)
