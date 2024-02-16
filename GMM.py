import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import GridSearchCV

# Iterate through sabe_dbs list
for idx, sabe_db in enumerate(sabe_dbs):
    # Extract the "Ratio" column from sabe_db
    X = sabe_db['Ratio'].values.reshape(-1, 1)  # Assuming 'Ratio' is the column name

    # Define a callable for BIC score
    def gmm_bic_score(estimator, X):
        return -estimator.bic(X)

    # Parameter grid for GridSearchCV
    param_grid = {
        "n_components": range(2, 7),
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

    # Export the results to a CSV file
    filename = file_names[idx]  # Assumes you have a corresponding filename for each DataFrame
    output_csv = f"{filename}_GMM_bic.csv"
    df.to_csv(output_csv, index=False)

    print(f"Results for {filename} exported to {output_csv}")
