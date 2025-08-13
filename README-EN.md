# Data Arrangement Version 4 - User Guide

## Overview

The Data arrangement Version 4.py script is a comprehensive tool that combines file classification and data arrangement functionality for the IGDB analysis process by QI Bio. It first organizes input files into a structured folder hierarchy, then processes the data to generate alignment (Precise Efficiency) and sum ratio (InDel) results.

## Prerequisites

### 1. Python Environment
- Python 3.6 or higher
- Required packages: pandas, os, shutil (all are standard library except pandas)
- Install pandas: `pip install pandas`

### 2. Required Files
- `relationship.csv` file (location input needed)
- Source data files (Excel .xls or CSV files, location input needed)

### 3. Directory Structure
- Source directory: enter the location of all the source data files
- All output files will be saved to the same source directory

## Input Data Format

### 1. RELATIONSHIP.CSV FILE FORMAT
The `relationship.csv` file must contain the following columns:
- **Name**: The classification name that matches your source file names
- **Case**: Either "point mutation" or "others"
- **Target_Sequence**: The sequence to search for in the data files

**Example relationship.csv:**
```csv
Name,Case,Target_Sequence
Sample1,point mutation,ATCG
Sample2,others,GCTA
```

### 2. SOURCE DATA FILE NAMING CONVENTION
Files must follow one of these naming patterns in the sample_sheet provided to Qibio:

**Pattern 1 (Hyphen-separated):** `"Name-number-whatever"`
- Example: `DMD-01-Treated`, `COX2-02-control`

**Pattern 2 (Underscore-separated):** `"prefix_Name_whatever"`
- Example: `0702_DMD_crRNA1`, `0703_DMD_crRNA2`

### 3. SUPPORTED FILE TYPES
- `.xls` (Excel files)
- `.csv` (Comma-separated values)

### 4. REQUIRED FILE TYPE IDENTIFIERS
Your source files must contain one of these identifiers in the filename:
- `.detail` (for detail files)
- `.Indeldetail` (for Indeldetail files)
- `.Count` (for count files - will be deleted after processing)
- `.Percent` (for percent files - will be deleted after processing)

### 5. CSV DATA STRUCTURE REQUIREMENTS
The CSV files must contain:
- A "Key" column containing sequence data
- A "Ratio" column (for Indeldetail files)
- A "Ratio(%)" column (for detail files with point mutations)

## How to Use

### Step 1: Prepare Your Data
1. Place your source data files in your desired directory (e.g., `C:/Users/lkmbi/Desktop/0617-WS1`)
2. Ensure your `relationship.csv` file is at your desired location (e.g., `C:/Users/lkmbi/Desktop/relationship.csv`)
3. Verify all files follow the required naming conventions

### Step 2: Run the Script
1. Open Command Prompt or PowerShell
2. Navigate to the directory containing `Data arrangement Version4.py`
3. Run the command: `python "Data arrangement Version4.py"`

### Step 3: Monitor Progress
The script will display progress messages:
- "Starting file classification process..."
- File movement confirmations
- Folder deletion confirmations
- "File classification completed!"
- "Starting data arrangement process..."
- Individual result file creation confirmations
- "All combined results saved to: [path]"
- "Combined processing completed successfully!"

## Processing Steps

### Phase 1: File Classification
1. Scans the source directory for .xls and .csv files
2. Extracts classification names from filenames
3. Identifies file types (detail, Indeldetail, Count, Percent)
4. Creates folder structure: `[SourceDir]/[Classification]/[FileType]/`
5. Moves files to appropriate folders
6. Deletes Count and Percent folders (not needed for analysis)

### Phase 2: Data Arrangement
1. Reads the `relationship.csv` file
2. For each relationship entry:
   - Processes alignment results based on case type
   - Calculates total alignment ratios
   - Processes sum results from Indeldetail folders
   - Combines alignment and sum data
   - Saves individual combined results files
3. Merges all individual results into a final comprehensive file

## Output Files

### 1. Organized Folder Structure
```
C:/Users/lkmbi/Desktop/0617-WS1/
├── [Classification1]/
│   ├── detail/
│   │   └── [detail files]
│   └── Indeldetail/
│       └── [Indeldetail files]
├── [Classification2]/
│   ├── detail/
│   └── Indeldetail/
└── ...
```

### 2. Individual Result Files
- `[Classification]_combined_results.csv`
- Contains columns: Filename Alignment, Total Alignment Ratio, Total Sum Ratio, Filename Sum

### 3. Final Comprehensive File
- `all_combined_results.csv`
- Contains all individual results plus a "Name" column
- Located at: `C:/Users/lkmbi/Desktop/0617-WS1/all_combined_results.csv`

## Output Data Format

The final `all_combined_results.csv` contains:
- **Filename Alignment**: Name of the alignment file processed
- **Total Alignment Ratio**: Sum of alignment ratios for target sequence
- **Total Sum Ratio**: Sum of all ratios in the Indeldetail file
- **Filename Sum**: Name of the sum file processed
- **Name**: Classification name (folder name)

## Error Handling

The script handles various error scenarios:
1. Files without proper naming conventions are skipped
2. Missing folders are created automatically
3. Non-numeric ratio values are converted to 0
4. Missing columns are handled gracefully
5. File read errors are caught and reported

**Common error messages:**
- "Skipping [filename]: No underscore or hyphen found in filename"
- "Skipping [filename]: No recognized file type pattern found"
- "Error processing [filename]: [error details]"

## Troubleshooting

### 1. "File not found" errors:
- Check that `relationship.csv` exists at the specified path
- Verify source directory path is correct

### 2. "No files processed":
- Ensure source files follow naming conventions
- Check file extensions (.xls or .csv)

### 3. "Empty results":
- Verify CSV files contain required columns (Key, Ratio, Ratio(%))
- Check that target sequences exist in the data

### 4. "Permission errors":
- Ensure you have write permissions to the source directory
- Close any open Excel files before running the script

## Customization

To modify paths or behavior:
1. Edit the source_directory variable in the script
2. Edit the relationship_file path in the script
3. Modify file type identifiers in the `classify_files()` function
4. Adjust column names in `process_alignment_results()` and `process_sum_results()`

## Support

For issues or questions:
1. Check the error messages in the console output
2. Verify all input files follow the required format
3. Ensure all prerequisites are met
4. Check file permissions and paths

## Version Information

- **Script**: `Data arrangement Version4.py`
- **Function**: File classification and data arrangement
- **Dependencies**: pandas, os, shutil
- **Compatibility**: Python 3.6+
- **Last Updated**: Current Date

---

**Developer**: Li KA MING

## License

This project is licensed under the MIT License. See the LICENSE file for details.

Copyright (c) 2024 Li KA MING. All rights reserved.
