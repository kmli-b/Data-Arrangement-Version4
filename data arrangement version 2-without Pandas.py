import os
import csv

# Define the folders for alignment results and sum results
alignment_folder_path = 'C:/Users/LKM/Desktop/ciPE/Miseq data/11_08/Detail_Result/HEK4/detail'
sum_folder_path = 'C:/Users/LKM/Desktop/ciPE/Miseq data/11_08/Detail_Result/HEK4/Indeldetail'

# Define the target sequence for alignment results
target_sequence = "TGCGGCTGGAGGTGG"

# Function to process alignment results
def process_alignment_results(folder_path, target_sequence):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    alignment_results = []

    for file_name in csv_files:
        file_path = os.path.join(folder_path, file_name)
        total_ratio = 0

        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if the "Key" column matches the target sequence
                if row.get("Key") == target_sequence:
                    try:
                        total_ratio += float(row.get("Ratio(%)", 0))
                    except ValueError:
                        pass

        alignment_results.append([file_name, total_ratio])

    return [["Filename", "Total Alignment Ratio(%)"]] + alignment_results

# Function to process sum results
def process_sum_results(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    sum_results = []

    for file_name in csv_files:
        file_path = os.path.join(folder_path, file_name)
        total_ratio = 0

        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Sum the "Ratio" column if it exists
                try:
                    total_ratio += float(row.get("Ratio", 0))
                except ValueError:
                    pass

        sum_results.append([file_name, total_ratio])

    return [["Filename", "Total Sum Ratio"]] + sum_results

# Save the results to a CSV file
def save_to_csv(file_path, data):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

# Process both results
alignment_results = process_alignment_results(alignment_folder_path, target_sequence)
sum_results = process_sum_results(sum_folder_path)

# Save results to CSV files
output_file1_path = 'C:/Users/LKM/Desktop/HEK4_Total_results-1.csv'
save_to_csv(output_file1_path, alignment_results)
print(f"Alignment results saved to: {output_file1_path}")

output_file2_path = 'C:/Users/LKM/Desktop/HEK4_Indel_results-1.csv'
save_to_csv(output_file2_path, sum_results)
print(f"Sum results saved to: {output_file2_path}")
