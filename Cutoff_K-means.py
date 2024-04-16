import os
import pandas as pd
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.interpolate import interp1d
import argparse

# Argument parser setup
parser = argparse.ArgumentParser(description='Calculate optimal cutoffs for classification models.')
parser.add_argument('--modresult_folder', type=str, help='Path to the folder containing modresult CSV files.')
parser.add_argument('--unmodresult_folder', type=str, help='Path to the folder containing unmodresult CSV files.')
parser.add_argument('--output_file', type=str, help='Path to save the optimal cutoffs CSV file.')
args = parser.parse_args()

# Assigning values from command-line arguments or using defaults
modresult_folder = args.modresult_folder if args.modresult_folder else "/home/share/shenglun/workspace/m1apre/quantitative/cutoffupdate/modresult"
unmodresult_folder = args.unmodresult_folder if args.unmodresult_folder else "/home/share/shenglun/workspace/m1apre/quantitative/cutoffupdate/unmodresult"
output_file = args.output_file if args.output_file else "/home/share/shenglun/workspace/m1apre/quantitative/cutoffupdate/optimal_cutoffnew.csv"

# Get all CSV files in modresult folder
modresult_files = [file for file in os.listdir(modresult_folder) if file.endswith('.csv')]

# Store optimal cutoff values for each file
optimal_cutoffs = {'File': [], 'Optimal_Cutoff': []}

# Define objective function for optimization
def objective(cutoff, mod_probs, unmod_probs_interp):
    mod_labels = (mod_probs >= cutoff).astype(int)
    unmod_labels = (unmod_probs_interp >= cutoff).astype(int)
    return -np.mean(np.abs(mod_labels - unmod_labels))  # Minimize the mean absolute difference between two sets of labels

# Process each modresult file
for mod_file in modresult_files:
    # Read modresult file
    modresult_file_path = os.path.join(modresult_folder, mod_file)
    modresult_df = pd.read_csv(modresult_file_path)
    
    # Find the corresponding unmodresult file
    unmodresult_file_path = os.path.join(unmodresult_folder, mod_file)

    # If the corresponding unmodresult file exists, read the data
    if os.path.exists(unmodresult_file_path):
        unmodresult_df = pd.read_csv(unmodresult_file_path)
    else:
        print(f"unmodresult file not found for {mod_file}. Skipping...")
        continue
    
    # Extract Probability column data
    mod_probs = modresult_df['Probability'].values
    unmod_probs = unmodresult_df['Probability'].values
    
    # Interpolate unmod_probs to match the length of mod_probs
    unmod_probs_interp = interp1d(np.linspace(0, 1, len(unmod_probs)), unmod_probs)(np.linspace(0, 1, len(mod_probs)))
    
    # Use optimization algorithm to find the optimal cutoff value
    result = minimize_scalar(objective, args=(mod_probs, unmod_probs_interp), bounds=(0, 1), method='bounded')
    
    # Record the optimal cutoff value for each file
    optimal_cutoffs['File'].append(mod_file)
    optimal_cutoffs['Optimal_Cutoff'].append(result.x)

# Create DataFrame to store the final results
optimal_cutoffs_df = pd.DataFrame(optimal_cutoffs)

# Save the results to a new file
optimal_cutoffs_df.to_csv(output_file, index=False)

print(f"Optimal cutoff values saved to: {output_file}")
