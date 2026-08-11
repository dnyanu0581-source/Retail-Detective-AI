import json
import pandas as pd

from config.db_config import get_connection


# ============================================================
# DATASET METADATA
# ============================================================

def create_dataset(
    user_id,
    filename,
    file_type,
    row_count,
    column_count
):
    """
    Create a dataset record in PostgreSQL.

    Returns:
        dataset_id if successful
        None if failed
    """

    connection = get_connection()

    if connection is None:
        return None

    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO datasets (
                user_id,
                filename,
                file_type,
                row_count,
                column_count,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """

        cursor.execute(
            query,
            (
                user_id,
                filename,
                file_type,
                row_count,
                column_count,
                "uploaded"
            )
        )

        dataset_id = cursor.fetchone()[0]

        connection.commit()

        return dataset_id

    except Exception as e:
        connection.rollback()
        print(f"Dataset creation error: {e}")
        return None

    finally:
        cursor.close()
        connection.close()


# ============================================================
# SAVE DATASET ROWS
# ============================================================

def save_dataset_rows(dataset_id, dataframe, data_version="raw"):
    """
    Store DataFrame rows in PostgreSQL JSONB.

    Converts Pandas/NumPy missing values such as:
        NaN
        NaT
        None

    into JSON-compatible null values.

    data_version:
        raw
        cleaned
    """

    if dataframe is None:
        return False

    if dataframe.empty:
        return False

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:

        query = """
            INSERT INTO dataset_rows (
                dataset_id,
                row_data,
                data_version
            )
            VALUES (%s, %s::jsonb, %s)
        """

        # Convert DataFrame into records
        rows = dataframe.to_dict(orient="records")

        for row in rows:

            json_safe_row = {}

            for column, value in row.items():

                # ------------------------------------------------
                # Convert Pandas / NumPy missing values to None
                # ------------------------------------------------
                if value is None:
                    json_safe_row[column] = None
                    continue

                try:

                    if pd.isna(value):
                        json_safe_row[column] = None
                        continue

                except (TypeError, ValueError):
                    pass

                # ------------------------------------------------
                # Convert NumPy scalar values to Python values
                # ------------------------------------------------
                if hasattr(value, "item"):

                    try:
                        value = value.item()

                    except (ValueError, TypeError):
                        value = str(value)

                # ------------------------------------------------
                # Convert dates / timestamps to strings
                # ------------------------------------------------
                if hasattr(value, "isoformat"):

                    try:
                        value = value.isoformat()

                    except (ValueError, TypeError):
                        value = str(value)

                # ------------------------------------------------
                # Make sure the final value is JSON serializable
                # ------------------------------------------------
                try:

                    json.dumps(value)

                    json_safe_row[column] = value

                except (TypeError, ValueError):

                    json_safe_row[column] = str(value)

            cursor.execute(
                query,
                (
                    dataset_id,
                    json.dumps(json_safe_row),
                    data_version
                )
            )

        connection.commit()

        return True

    except Exception as e:

        connection.rollback()

        print(f"Dataset row storage error: {e}")

        return False

    finally:

        cursor.close()
        connection.close()
# ============================================================
# DELETE DATASET VERSION
# ============================================================

def delete_dataset_version(dataset_id, data_version):
    """
    Delete a particular version of dataset rows.

    Example:
        raw
        cleaned
    """

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:

        query = """
            DELETE FROM dataset_rows
            WHERE dataset_id = %s
            AND data_version = %s
        """

        cursor.execute(
            query,
            (
                dataset_id,
                data_version
            )
        )

        connection.commit()

        return True

    except Exception as e:

        connection.rollback()

        print(f"Dataset deletion error: {e}")

        return False

    finally:

        cursor.close()
        connection.close()


# ============================================================
# UPDATE DATASET STATUS
# ============================================================

def update_dataset_status(dataset_id, status):
    """
    Update dataset processing status.

    Examples:
        uploaded
        cleaning
        cleaned
        failed
    """

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:

        query = """
            UPDATE datasets
            SET status = %s
            WHERE id = %s
        """

        cursor.execute(
            query,
            (
                status,
                dataset_id
            )
        )

        connection.commit()

        return True

    except Exception as e:

        connection.rollback()

        print(f"Dataset status update error: {e}")

        return False

    finally:

        cursor.close()
        connection.close()


# ============================================================
# CLEANING LOG
# ============================================================

def create_cleaning_log(
    dataset_id,
    rows_before,
    rows_after,
    duplicates_removed,
    missing_values_before,
    missing_values_after
):
    """
    Store dataset cleaning information.
    """

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:

        query = """
            INSERT INTO cleaning_logs (
                dataset_id,
                rows_before,
                rows_after,
                duplicates_removed,
                missing_values_before,
                missing_values_after
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                dataset_id,
                rows_before,
                rows_after,
                duplicates_removed,
                missing_values_before,
                missing_values_after
            )
        )

        connection.commit()

        return True

    except Exception as e:

        connection.rollback()

        print(f"Cleaning log error: {e}")

        return False

    finally:

        cursor.close()
        connection.close()


# ============================================================
# GET DATASET INFORMATION
# ============================================================

def get_dataset(dataset_id):

    connection = get_connection()

    if connection is None:
        return None

    cursor = connection.cursor()

    try:

        query = """
            SELECT
                id,
                user_id,
                filename,
                file_type,
                uploaded_at,
                row_count,
                column_count,
                status
            FROM datasets
            WHERE id = %s
        """

        cursor.execute(
            query,
            (dataset_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "user_id": row[1],
            "filename": row[2],
            "file_type": row[3],
            "uploaded_at": row[4],
            "row_count": row[5],
            "column_count": row[6],
            "status": row[7]
        }

    except Exception as e:

        print(f"Dataset retrieval error: {e}")

        return None

    finally:

        cursor.close()
        connection.close()


# ============================================================
# GET USER DATASETS
# ============================================================

def get_user_datasets(user_id):

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor()

    try:

        query = """
            SELECT
                id,
                filename,
                file_type,
                uploaded_at,
                row_count,
                column_count,
                status
            FROM datasets
            WHERE user_id = %s
            ORDER BY uploaded_at DESC
        """

        cursor.execute(
            query,
            (user_id,)
        )

        rows = cursor.fetchall()

        datasets = []

        for row in rows:

            datasets.append({
                "id": row[0],
                "filename": row[1],
                "file_type": row[2],
                "uploaded_at": row[3],
                "row_count": row[4],
                "column_count": row[5],
                "status": row[6]
            })

        return datasets

    except Exception as e:

        print(f"User datasets retrieval error: {e}")

        return []

    finally:

        cursor.close()
        connection.close()
