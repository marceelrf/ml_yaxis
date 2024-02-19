import numpy as np
import pandas as pd
import os
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import GridSearchCV

folder_path = 'SABE/ncopy/plots/'

if not globals().get('sabe_dbs'):
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('plot_db.txt'):
                files.append(os.path.join(root, filename))

    file_names = [os.path.splitext(os.path.basename(file))[0] for file in files]
    sabe_dbs = []

    for file, file_name in zip(files, file_names):
        try:
            df = pd.read_csv(file, sep='\t')
            sabe_dbs.append(df)
            print(f"File '{file_name}' read successfully.")
        except FileNotFoundError:
            print(f"File '{file_name}' not found. Skipping.")


# Now, 'sabe_dbs' contains a list of DataFrames for existing files, and 'file_names' contains corresponding file names

output_folder = "output_GMM"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for idx, sabe_db in enumerate(sabe_dbs):
    # Extract the "Ratio" column from sabe_db
    X = sabe_db['Ratio'].values.reshape(-1, 1)  # Assuming 'Ratio' is the column name

    # Define a callable for BIC score
    def gmm_bic_score(estimator, X):
        return -estimator.bic(X)

    # Parameter grid for GridSearchCV
    param_grid = {
        "n_components": range(1, 7),
        "covariance_type": ["spherical", "tied", "diag", "full"],
    }

    # GridSearchCV
    grid_search = GridSearchCV(
        GaussianMixture(), param_grid=param_grid, scoring=gmm_bic_score
    )
    grid_search.fit(X)

    # Create DataFrame from grid search results
    df = pd.DataFrame(grid_search.cv_results_)[
        ["param_n_components", "param_covariance_type", "mean_test_score"]
    ]
    df["mean_test_score"] = -df["mean_test_score"]
    df = df.rename(
        columns={
            "param_n_components": "Number of components",
            "param_covariance_type": "Type of covariance",
            "mean_test_score": "BIC score",
        }
    )

    # Export the results to a CSV file in the output folder
    filename = file_names[idx]
    output_csv = os.path.join(output_folder, f"{filename}_GMM_bic.csv")
    df.to_csv(output_csv, index=False)

    print(f"Results for {filename} exported to {output_csv}")