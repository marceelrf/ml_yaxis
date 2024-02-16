import numpy as np
import pandas as pd
from sklearn.mixture import BayesianGaussianMixture
from sklearn.model_selection import GridSearchCV

# Iterate through sabe_dbs list
for idx, sabe_db in enumerate(sabe_dbs):
    # Extract the "Ratio" column from sabe_db
    X = sabe_db['Ratio'].values.reshape(-1, 1)  # Assuming 'Ratio' is the column name

    # Define a callable for BIC score
    def bgmm_bic_score(estimator, X):
        return -estimator.bic(X)

    # Parameter grid for GridSearchCV
    param_grid = {
        "n_components": range(1, 7),
        "covariance_type": ["spherical", "tied", "diag", "full"],
        "weight_concentration_prior_type": ["dirichlet_process", "dirichlet_distribution"],
    }

    # GridSearchCV
    grid_search = GridSearchCV(
        BayesianGaussianMixture(), param_grid=param_grid, scoring=bgmm_bic_score
    )
    grid_search.fit(X)

    # Create DataFrame from grid search results
    df = pd.DataFrame(grid_search.cv_results_)[
        ["param_n_components", "param_covariance_type", "param_weight_concentration_prior_type", "mean_test_score"]
    ]
    df["mean_test_score"] = -df["mean_test_score"]
    df = df.rename(
        columns={
            "param_n_components": "Number of components",
            "param_covariance_type": "Type of covariance",
            "param_weight_concentration_prior_type": "Weight Concentration Prior",
            "mean_test_score": "BIC score",
        }
    )

    # Export the results to a CSV file
    filename = file_names[idx]  # Assumes you have a corresponding filename for each DataFrame
    output_csv = f"{filename}_BGMM_bic.csv"
    df.to_csv(output_csv, index=False)

    print(f"Results for {filename} exported to {output_csv}")
