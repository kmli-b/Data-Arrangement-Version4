import pandas as pd
import os

# Function to process alignment results
def process_alignment_results(folder_path, target_sequence, case_type):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    alignment_results = []

    for file_name in csv_files:
        file_path = os.path.join(folder_path, file_name)
        data = pd.read_csv(file_path)

        # Case-insensitive search for target_sequence
        matched_data = data[data["Key"].str.contains(target_sequence, na=False, case=False)]

        # Determine the column name based on the case
        ratio_column = "Ratio(%)" if case_type == "point mutation" else "Ratio"

        if ratio_column in data.columns and not matched_data.empty:
            # Clean the ratio column by removing non-numeric values
            try:
                # Convert to numeric, coercing errors to NaN
                numeric_ratios = pd.to_numeric(matched_data[ratio_column], errors='coerce')
                # Remove NaN values and sum
                total_ratio = numeric_ratios.dropna().sum()
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
                total_ratio = 0
        else:
            total_ratio = 0
        
        alignment_results.append([file_name, total_ratio])
    
    return pd.DataFrame(alignment_results, columns=["Filename Alignment", "Total Alignment Ratio"])

# Function to process sum results
def process_sum_results(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    sum_results = []

    for file_name in csv_files:
        file_path = os.path.join(folder_path, file_name)
        data = pd.read_csv(file_path)
        
        if "Ratio" in data.columns:
            # Clean the ratio column by removing non-numeric values
            try:
                # Convert to numeric, coercing errors to NaN
                numeric_ratios = pd.to_numeric(data["Ratio"], errors='coerce')
                # Remove NaN values and sum
                total_ratio = numeric_ratios.dropna().sum()
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
                total_ratio = 0
        else:
            total_ratio = 0
        
        sum_results.append([file_name, total_ratio])
    
    return pd.DataFrame(sum_results, columns=["Filename Sum", "Total Sum Ratio"])

# Load the relationship file
relationship_file = 'C:/Users/lkmbi/Desktop/relationship.csv'  # Update the path
relationship_data = pd.read_csv(relationship_file)

# Define the base folder path
base_folder_path = 'C:/Users/lkmbi/Desktop/Detail_result_WYQ'  # Update the base directory path

# Iterate through the rows of the relationship file
for index, row in relationship_data.iterrows():
    name = row["Name"]
    case = row["Case"]
    target_sequence = row["Target_Sequence"]

    # Determine folder paths
    detail_folder_path = os.path.join(base_folder_path, name, "detail")
    indeldetail_folder_path = os.path.join(base_folder_path, name, "Indeldetail")

    # Process alignment results based on case
    if case == "point mutation":
        alignment_df = process_alignment_results(detail_folder_path, target_sequence, case)
    else:  # case == "others"
        alignment_df = process_alignment_results(indeldetail_folder_path, target_sequence, case)

    # Process sum results in Indeldetail folder
    sum_df = process_sum_results(indeldetail_folder_path)

    # # Save alignment results
    # alignment_output_path = os.path.join(base_folder_path, f"{name}_alignment_results.csv")
    # alignment_df.to_csv(alignment_output_path, index=False)
    # print(f"Alignment results saved to: {alignment_output_path}")

    # # Save sum results
    # sum_output_path = os.path.join(base_folder_path, f"{name}_sum_results.csv")
    # sum_df.to_csv(sum_output_path, index=False)
    # Combine the two DataFrames    
    combined_df = pd.concat([alignment_df, sum_df], axis=1)
    combined_df = combined_df[
        ["Filename Alignment", "Total Alignment Ratio", "Total Sum Ratio","Filename Sum"]
    ]  # Ensure the correct column order

    # Save the combined results to a CSV file
    combined_output_path = os.path.join(base_folder_path, f"{name}_combined_results.csv")
    combined_df.to_csv(combined_output_path, index=False)
    print(f"Combined results saved to: {combined_output_path}")

# Define a list to store DataFrames from all combined result files
all_combined_results = []

# Iterate through all files in the base folder
for folder_name in os.listdir(base_folder_path):
    folder_path = os.path.join(base_folder_path, folder_name)
    
    # Check if it's a folder
    if os.path.isdir(folder_path):
        combined_file_path = os.path.join(base_folder_path, f"{folder_name}_combined_results.csv")
        
        # Check if the combined results file exists
        if os.path.exists(combined_file_path):
            # Read the combined results file
            combined_df = pd.read_csv(combined_file_path)
            
            # Add a column for the folder name (Name)
            combined_df["Name"] = folder_name
            
            # Append to the list
            all_combined_results.append(combined_df)

# Concatenate all DataFrames into one
final_combined_df = pd.concat(all_combined_results, ignore_index=True)

# Save the final combined DataFrame to a single CSV file
final_output_path = os.path.join(base_folder_path, "all_combined_results.csv")
final_combined_df.to_csv(final_output_path, index=False)
print(f"All combined results saved to: {final_output_path}")