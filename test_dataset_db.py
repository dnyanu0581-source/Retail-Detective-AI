
import pandas as pd

from database.dataset_db import (
    create_dataset,
    save_dataset_rows,
    get_dataset
)


print("====================================")
print("Testing Dataset Row Storage")
print("====================================")


# Use an existing user ID from your users table
USER_ID = 1


# ------------------------------------------------------------
# Create a small test DataFrame
# ------------------------------------------------------------

data = {
    "Product": [
        "Laptop",
        "Mouse",
        "Keyboard",
        "Monitor",
        "Headphones"
    ],
    "Sales": [
        50000,
        2500,
        4500,
        30000,
        7000
    ],
    "Quantity": [
        5,
        10,
        8,
        3,
        7
    ]
}


df = pd.DataFrame(data)


print("\nTest DataFrame:")
print(df)


# ------------------------------------------------------------
# Create dataset record
# ------------------------------------------------------------

dataset_id = create_dataset(
    user_id=USER_ID,
    filename="dataframe_test.csv",
    file_type="csv",
    row_count=len(df),
    column_count=len(df.columns)
)


if dataset_id is None:

    print("\n❌ Dataset creation failed.")

    raise SystemExit


print(f"\n✅ Dataset created!")
print(f"Dataset ID: {dataset_id}")


# ------------------------------------------------------------
# Save DataFrame rows
# ------------------------------------------------------------

result = save_dataset_rows(
    dataset_id=dataset_id,
    dataframe=df,
    data_version="raw"
)


if result:

    print("✅ DataFrame successfully stored in PostgreSQL.")

else:

    print("❌ DataFrame storage failed.")


# ------------------------------------------------------------
# Retrieve dataset metadata
# ------------------------------------------------------------

dataset = get_dataset(dataset_id)


if dataset:

    print("\n====================================")
    print("Dataset Information")
    print("====================================")

    print("ID:", dataset["id"])
    print("User ID:", dataset["user_id"])
    print("Filename:", dataset["filename"])
    print("Rows:", dataset["row_count"])
    print("Columns:", dataset["column_count"])
    print("Status:", dataset["status"])

else:

    print("❌ Could not retrieve dataset.")

