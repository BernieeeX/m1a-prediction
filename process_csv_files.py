import os
import csv
import argparse

def process_csv_files(csv_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    data_dict = {}

    for csv_file_name in os.listdir(csv_folder):
        if csv_file_name.endswith('.csv'):
            csv_file_path = os.path.join(csv_folder, csv_file_name)

            with open(csv_file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)  
                for row in csv_reader:
                    value_in_column_5 = row[5] 

                    if value_in_column_5 in data_dict:
                        data_dict[value_in_column_5].append(row)
                    else:
                        data_dict[value_in_column_5] = [row]

    for key, data_list in data_dict.items():
        output_file_path = os.path.join(output_folder, f"{key}.csv")
        with open(output_file_path, 'w', newline='') as output_file:
            csv_writer = csv.writer(output_file)
            csv_writer.writerow(header) 
            csv_writer.writerows(data_list)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CSV files and divide them based on column 5 values.")
    parser.add_argument("-i", "--input", help="Input folder containing CSV files", required=True)
    parser.add_argument("-o", "--output", help="Output folder for divided CSV files", required=True)
    args = parser.parse_args()

    process_csv_files(args.input, args.output)
