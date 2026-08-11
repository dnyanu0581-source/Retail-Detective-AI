import pandas as pd

from database.dataset_db import (
    create_dataset,
    save_dataset_rows,
    get_dataset
)

# ------------------------------------------------------------
# TEST DATA
# ------------------------------------------------------------

df = pd.DataFrame({
    "Name": ["Amit", "Priya", "Rahul"],
    "Age": [21, 22, 20],
    "Sales": [1500, 2300, 1800]
})


# ------------------------------------------------------------
# CREATE DATASET RECORD
# ------------------------------------------------------------

dataset_id = create_dataset(
    user_id=1,
    filename="test_dataset.csv",
    file_type="csv",
    row_count=len(df),
    column_count=len(df.columns)
)

print("Dataset ID:", dataset_id)


# ------------------------------------------------------------
# SAVE DATASET ROWS
# ------------------------------------------------------------

if dataset_id:

    success = save_dataset_rows(
        dataset_id=dataset_id,
        dataframe=df,
        data_version="raw"
    )

    print("Rows saved:", success)


# ------------------------------------------------------------
# GET DATASET INFORMATION
# ------------------------------------------------------------

if dataset_id:

    dataset = get_dataset(dataset_id)

    print("\nDataset information:")
    print(dataset)