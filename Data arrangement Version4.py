import pandas as pd
import os
import shutil

# Remove hardcoded source_directory and relationship_file

def classify_files(source_directory):
    """First function: Classify and organize files into folders"""
    print("Starting file classification process...")
    
    # List all the files in the source directory
    file_list = [f for f in os.listdir(source_directory) if f.endswith('.xls') or f.endswith('.csv')]

    # Process each file
    for file_name in file_list:
        # Check if the file name has the expected separator pattern (underscore or hyphen)
        if '_' not in file_name and '-' not in file_name:
            print(f'Skipping {file_name}: No underscore or hyphen found in filename')
            continue
        
        # Split the file name to extract the classification part and the file type part
        # For new format "Name-number-label", extract the name before first hyphen
        if '-' in file_name:
            name_parts = file_name.split('-')
            classification = name_parts[0]  # Take the part before the first hyphen
        elif '_' in file_name:
            name_parts = file_name.split('_')
            classification = name_parts[1]  # Keep original logic for underscore format
        else:
            print(f'Skipping {file_name}: No valid separator found')
            continue
        
        if len(name_parts) < 2:
            print(f'Skipping {file_name}: Not enough parts after splitting by separator')
            continue
        
        # Identify the type of the file from the file extension part after the last period
        if '.detail' in file_name:
            file_type = 'detail'
        elif '.Indeldetail' in file_name:
            file_type = 'Indeldetail'
        elif '.Count' in file_name:
            file_type = 'Count'
        elif '.Percent' in file_name:
            file_type = 'Percent'
        else:
            print(f'Skipping {file_name}: No recognized file type pattern found')
            continue  # Skip files that don't match the expected patterns

        # Define the target subfolder based on classification and file type
        target_directory = os.path.join(source_directory, classification, file_type)

        # Create the subfolder if it does not exist
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        # Move the file to the appropriate subfolder
        source_path = os.path.join(source_directory, file_name)
        target_path = os.path.join(target_directory, file_name)
        shutil.move(source_path, target_path)

        print(f'Moved {file_name} to {target_directory}')

    # After organizing, delete the 'Count' and 'Percent' folders
    for classification_folder in os.listdir(source_directory):
        classification_path = os.path.join(source_directory, classification_folder)
        
        # Ensure that we are looking at a folder
        if os.path.isdir(classification_path):
            # Paths to the 'Count' and 'Percent' folders
            count_folder = os.path.join(classification_path, 'Count')
            percent_folder = os.path.join(classification_path, 'Percent')
            
            # Delete the 'Count' folder if it exists
            if os.path.exists(count_folder):
                shutil.rmtree(count_folder)
                print(f'Deleted {count_folder}')

            # Delete the 'Percent' folder if it exists
            if os.path.exists(percent_folder):
                shutil.rmtree(percent_folder)
                print(f'Deleted {percent_folder}')
    
    print("File classification completed!")

def process_alignment_results(folder_path, target_sequence, case_type):
    """Function to process alignment results"""
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

def process_sum_results(folder_path):
    """Function to process sum results"""
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

def arrange_data(base_folder_path, relationship_file, output_folder_path):
    """Second function: Process and arrange data using the classified files"""
    print("Starting data alignment and sum process...")
    
    # Load the relationship file
    relationship_data = pd.read_csv(relationship_file)

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

        # Combine the two DataFrames    
        combined_df = pd.concat([alignment_df, sum_df], axis=1)
        combined_df = combined_df[
            ["Filename Alignment", "Total Alignment Ratio", "Total Sum Ratio","Filename Sum"]
        ]  # Ensure the correct column order

        # Save the combined results to a CSV file in the output folder
        combined_output_path = os.path.join(output_folder_path, f"{name}_combined_results.csv")
        combined_df.to_csv(combined_output_path, index=False)
        print(f"Combined results saved to: {combined_output_path}")

    # Define a list to store DataFrames from all combined result files
    all_combined_results = []

    # Iterate through all files in the output folder
    for file in os.listdir(output_folder_path):
        if file.endswith('_combined_results.csv') and file != 'all_combined_results.csv':
            combined_file_path = os.path.join(output_folder_path, file)
            combined_df = pd.read_csv(combined_file_path)
            # Add a column for the name (extracted from filename)
            folder_name = file.replace('_combined_results.csv', '')
            combined_df["Name"] = folder_name
            all_combined_results.append(combined_df)

    # Concatenate all DataFrames into one
    final_combined_df = pd.concat(all_combined_results, ignore_index=True)

    # Save the final combined DataFrame to a single CSV file in the output folder
    final_output_path = os.path.join(output_folder_path, "all_combined_results.csv")
    final_combined_df.to_csv(final_output_path, index=False)
    print(f"All combined results saved to: {final_output_path}")
    print("Data arrangement completed!")

def main():
    """Main function to run both processes in sequence"""
    print("Starting combined file processing...")
    
    # Prompt user for input and output locations
    source_directory = input("Enter the input (source) directory containing the data files: ").strip()
    relationship_file = input("Enter the path to the relationship CSV file: ").strip()
    output_folder_path = input("Enter the output directory for the results: ").strip()

    # Step 1: Classify and organize files
    classify_files(source_directory)
    
    # Step 2: Process and arrange data using the organized files
    arrange_data(source_directory, relationship_file, output_folder_path)
    
    print("Combined processing completed successfully!")

if __name__ == "__main__":
    main() 