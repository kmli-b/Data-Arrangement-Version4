import pandas as pd 
import os

# Define the folders for alignment results and sum results
alignment_folder_path = 'C:/Users/lkmbi/Desktop/0503/HEK4/Indeldetail'
sum_folder_path = 'C:/Users/lkmbi/Desktop/0503/HEK4/Indeldetail'

# Define the target sequence for alignment results
target_sequence = "TGCGGCTGGTGGGGGTT"

# Function to process alignment results
def process_alignment_results(folder_path, target_sequence):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    alignment_results = []

    for file_name in csv_files:
        file_path = os.path.join(folder_path, file_name)
        data = pd.read_csv(file_path)
        
        # Filter the data for rows where the "Key" column matches the target sequence without substring and case restriction
        #matched_data = data[data["Key"].str.contains(target_sequence,na=False,case=False)]

        # Filter the data for rows where the "Key" column exactly matches the target sequence 
        matched_data = data[data["Key"] == target_sequence]

        if not matched_data.empty:
            total_ratio = matched_data["Ratio"].astype(float).sum()
        else:
            total_ratio = 0
        
        alignment_results.append([file_name, total_ratio])
    
    return pd.DataFrame(alignment_results, columns=["Filename", "Total Alignment Ratio(%)"])

# Function to process sum results
def process_sum_results(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    sum_results = []

    for file_name in csv_files:
        file_path = os.path.join(folder_path, file_name)
        data = pd.read_csv(file_path)
        
        if "Ratio" in data.columns:
            total_ratio = data["Ratio"].astype(float).sum()
        else:
            total_ratio = 0
        
        sum_results.append([file_name, total_ratio])
    
    return pd.DataFrame(sum_results, columns=["Filename", "Total Sum Ratio"])

# Process both results
alignment_df = process_alignment_results(alignment_folder_path, target_sequence)
sum_df = process_sum_results(sum_folder_path)

#Save each result to a single CSV file
output_file1_path = 'C:/Users/lkmbi/Desktop/HEK4_efficiency_results-1.csv'
alignment_df.to_csv(output_file1_path, index=False)
print(f"Combined output saved to: {output_file1_path}")

output_file2_path = 'C:/Users/lkmbi/Desktop/HEK4_Indel_results-1.csv'
sum_df.to_csv(output_file2_path, index=False)
print(f"Combined output saved to: {output_file2_path}")