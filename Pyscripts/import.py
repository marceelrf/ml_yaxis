import os
import pandas as pd

# Directory containing your files
folder_path = 'SABE/ncopy/plots/'

# List all files with the pattern "plot_db.txt" in the specified folder and its subdirectories
files = []
for root, dirs, filenames in os.walk(folder_path):
    for filename in filenames:
        if filename.endswith('plot_db.txt'):
            files.append(os.path.join(root, filename))

# Extract file names
file_names = [os.path.splitext(os.path.basename(file))[0] for file in files]
file_names
# Read files into a list of DataFrames
sabe_dbs = [pd.read_csv(file, sep='\t') for file in files]
sabe_dbs
# Now, 'sabe_dbs' contains a list of DataFrames, and 'file_names' contains corresponding file names
