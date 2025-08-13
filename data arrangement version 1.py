import pandas as pd
import os

# Folder containing the CSV files
folder_path = '/path_to_your_folder/'

# Define the target sequence
target_sequence = "CGCTGGATACTTTCC"

# Get a list of all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Initialize an empty list to store results
final_output = []

# Loop through each CSV file, process the data, and append the results
for file_name in csv_files:
    file_path = os.path.join(folder_path, file_name)
    
    # Load the dataset
    data = pd.read_csv(file_path)
    
    # Filter the data for rows where the "Key" column matches the target sequence
    matched_data = data[data["Key"] == target_sequence]
    
    # If a match is found, sum the "Ratio(%)" column
    if not matched_data.empty:
        total_ratio = matched_data["Ratio(%)"].astype(float).sum()
    else:
        # If no match is found, set the total_ratio to 0
        total_ratio = 0
    
    # Append the result (filename and total_ratio) to the final output list
    final_output.append([file_name, total_ratio])

# Convert the list to a DataFrame
output_df = pd.DataFrame(final_output, columns=["Filename", "Total Ratio(%)"])

# Save the final output to a single CSV file
output_file_path = '/path_to_your_output/final_ratio_summary.csv'
output_df.to_csv(output_file_path, index=False)

print(f"Final output saved to: {output_file_path}")


# Initialize an empty list to store results
final_output = []

# Loop through each CSV file, process the data, and append the results
for file_name in csv_files:
    file_path = os.path.join(folder_path, file_name)
    
    # Load the dataset
    data = pd.read_csv(file_path)
    
    # Sum the "Ratio(%)" column if it exists
    if "Ratio(%)" in data.columns:
        total_ratio = data["Ratio(%)"].astype(float).sum()
    else:
        total_ratio = 0  # If the column doesn't exist, set the sum to 0
    
    # Append the result (filename and total_ratio) to the final output list
    final_output.append([file_name, total_ratio])

# Convert the list to a DataFrame
output_df = pd.DataFrame(final_output, columns=["Filename", "Total Ratio(%)"])

# Save the final output to a single CSV file
output_file_path = '/path_to_your_output/final_ratio_summary.csv'
output_df.to_csv(output_file_path, index=False)

print(f"Final output saved to: {output_file_path}")