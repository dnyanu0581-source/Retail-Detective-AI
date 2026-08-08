import pandas as pd
import re


# ============================================================
# COLUMN DETECTION
# ============================================================

def find_column_from_question(df, question):
    """
    Try to identify a dataset column mentioned in the question.
    """

    question_lower = question.lower()

    # --------------------------------------------------------
    # Exact column name
    # --------------------------------------------------------

    for column in df.columns:

        column_name = str(column).lower().strip()

        if column_name in question_lower:
            return column

    # --------------------------------------------------------
    # Normalized column name
    # Example:
    # customer_id -> customer id
    # total-sales -> total sales
    # --------------------------------------------------------

    for column in df.columns:

        normalized_column = (
            str(column)
            .lower()
            .strip()
            .replace("_", " ")
            .replace("-", " ")
        )

        if normalized_column in question_lower:
            return column

    # --------------------------------------------------------
    # Individual words from column name
    # --------------------------------------------------------

    for column in df.columns:

        normalized_column = (
            str(column)
            .lower()
            .strip()
            .replace("_", " ")
            .replace("-", " ")
        )

        column_words = normalized_column.split()

        if len(column_words) > 1:

            if all(
                word in question_lower
                for word in column_words
            ):
                return column

    return None


# ============================================================
# ANSWER QUESTION
# ============================================================

def answer_question(df, question):
    """
    Analyze the dataset and answer a natural-language question.
    """

    if df is None:

        return (
            "❌ No dataset is available."
        )

    if df.empty:

        return (
            "❌ The dataset is empty."
        )

    question = question.strip()

    question_lower = question.lower()

    # ========================================================
    # ROW COUNT
    # ========================================================

    if (
        "how many rows" in question_lower
        or "number of rows" in question_lower
        or "total rows" in question_lower
        or "how many records" in question_lower
        or "number of records" in question_lower
        or "total records" in question_lower
    ):

        return (
            f"📊 The dataset contains "
            f"**{len(df):,} rows**."
        )

    # ========================================================
    # COLUMN COUNT
    # ========================================================

    if (
        "how many columns" in question_lower
        or "number of columns" in question_lower
        or "total columns" in question_lower
    ):

        return (
            f"📊 The dataset contains "
            f"**{len(df.columns):,} columns**."
        )

    # ========================================================
    # COLUMN NAMES
    # ========================================================

    if (
        "what columns" in question_lower
        or "which columns" in question_lower
        or "list columns" in question_lower
        or "column names" in question_lower
        or "show columns" in question_lower
    ):

        columns = "\n".join(
            f"- **{column}**"
            for column in df.columns
        )

        return (
            "📋 **Columns in the dataset:**\n\n"
            + columns
        )

    # ========================================================
    # MISSING VALUES
    # ========================================================

    if (
        "missing values" in question_lower
        or "missing data" in question_lower
        or "null values" in question_lower
        or "null data" in question_lower
        or "empty values" in question_lower
    ):

        total_missing = int(
            df.isnull().sum().sum()
        )

        if total_missing == 0:

            return (
                "✅ There are **no missing values** "
                "in the dataset."
            )

        missing_columns = (
            df.isnull()
            .sum()
        )

        missing_columns = (
            missing_columns[
                missing_columns > 0
            ]
            .sort_values(
                ascending=False
            )
        )

        result = "\n".join(
            f"- **{column}**: "
            f"{int(value):,} missing"
            for column, value
            in missing_columns.items()
        )

        return (
            f"⚠️ The dataset contains "
            f"**{total_missing:,} missing values**.\n\n"
            f"### Missing values by column\n\n"
            f"{result}"
        )

    # ========================================================
    # DUPLICATES
    # ========================================================

    if (
        "duplicate rows" in question_lower
        or "duplicate records" in question_lower
        or "duplicates" in question_lower
    ):

        duplicate_count = int(
            df.duplicated().sum()
        )

        if duplicate_count == 0:

            return (
                "✅ There are **no duplicate rows**."
            )

        return (
            f"⚠️ The dataset contains "
            f"**{duplicate_count:,} duplicate rows**."
        )

    # ========================================================
    # NUMERIC COLUMNS
    # ========================================================

    if (
        "numeric columns" in question_lower
        or "numerical columns" in question_lower
        or "number columns" in question_lower
    ):

        numeric_columns = list(
            df.select_dtypes(
                include=["number"]
            ).columns
        )

        if not numeric_columns:

            return (
                "❌ No numeric columns were detected."
            )

        result = "\n".join(
            f"- **{column}**"
            for column in numeric_columns
        )

        return (
            "🔢 **Numeric columns:**\n\n"
            + result
        )

    # ========================================================
    # CATEGORICAL COLUMNS
    # ========================================================

    if (
        "categorical columns" in question_lower
        or "category columns" in question_lower
        or "text columns" in question_lower
    ):

        categorical_columns = list(
            df.select_dtypes(
                include=[
                    "object",
                    "category"
                ]
            ).columns
        )

        if not categorical_columns:

            return (
                "❌ No categorical columns were detected."
            )

        result = "\n".join(
            f"- **{column}**"
            for column in categorical_columns
        )

        return (
            "🔤 **Categorical columns:**\n\n"
            + result
        )

    # ========================================================
    # UNIQUE VALUES
    # ========================================================

    if (
        "unique values" in question_lower
        or "distinct values" in question_lower
    ):

        result = "\n".join(
            f"- **{column}**: "
            f"{df[column].nunique(dropna=True):,}"
            for column in df.columns
        )

        return (
            "🔢 **Unique values by column:**\n\n"
            + result
        )

    # ========================================================
    # FIND COLUMN
    # ========================================================

    selected_column = find_column_from_question(
        df,
        question_lower
    )

    # ========================================================
    # AVERAGE / MEAN
    # ========================================================

    if (
        "average" in question_lower
        or "mean" in question_lower
    ):

        numeric_columns = list(
            df.select_dtypes(
                include=["number"]
            ).columns
        )

        if selected_column is not None:

            if selected_column not in numeric_columns:

                return (
                    f"⚠️ **{selected_column}** is not "
                    f"a numeric column, so an average "
                    f"cannot be calculated."
                )

            value = (
                pd.to_numeric(
                    df[selected_column],
                    errors="coerce"
                )
                .mean()
            )

            return (
                f"📊 The average of "
                f"**{selected_column}** is "
                f"**{value:,.2f}**."
            )

        if len(numeric_columns) == 1:

            column = numeric_columns[0]

            value = (
                pd.to_numeric(
                    df[column],
                    errors="coerce"
                )
                .mean()
            )

            return (
                f"📊 The average of "
                f"**{column}** is "
                f"**{value:,.2f}**."
            )

        return (
            "🔎 Please specify a numeric column "
            "for the average."
        )

    # ========================================================
    # MEDIAN
    # ========================================================

    if "median" in question_lower:

        numeric_columns = list(
            df.select_dtypes(
                include=["number"]
            ).columns
        )

        if selected_column is not None:

            if selected_column not in numeric_columns:

                return (
                    f"⚠️ **{selected_column}** is not "
                    f"a numeric column."
                )

            value = (
                pd.to_numeric(
                    df[selected_column],
                    errors="coerce"
                )
                .median()
            )

            return (
                f"📊 The median of "
                f"**{selected_column}** is "
                f"**{value:,.2f}**."
            )

        if len(numeric_columns) == 1:

            column = numeric_columns[0]

            value = (
                pd.to_numeric(
                    df[column],
                    errors="coerce"
                )
                .median()
            )

            return (
                f"📊 The median of "
                f"**{column}** is "
                f"**{value:,.2f}**."
            )

        return (
            "🔎 Please specify a numeric column "
            "for the median."
        )

    # ========================================================
    # MINIMUM
    # ========================================================

    if (
        "minimum" in question_lower
        or "minimum value" in question_lower
        or "lowest" in question_lower
        or "smallest" in question_lower
    ):

        numeric_columns = list(
            df.select_dtypes(
                include=["number"]
            ).columns
        )

        if selected_column is not None:

            if selected_column not in numeric_columns:

                return (
                    f"⚠️ **{selected_column}** is not "
                    f"a numeric column."
                )

            value = (
                pd.to_numeric(
                    df[selected_column],
                    errors="coerce"
                )
                .min()
            )

            return (
                f"📉 The minimum value of "
                f"**{selected_column}** is "
                f"**{value:,.2f}**."
            )

        if len(numeric_columns) == 1:

            column = numeric_columns[0]

            value = (
                pd.to_numeric(
                    df[column],
                    errors="coerce"
                )
                .min()
            )

            return (
                f"📉 The minimum value of "
                f"**{column}** is "
                f"**{value:,.2f}**."
            )

        return (
            "🔎 Please specify which numeric "
            "column you want the minimum value for."
        )

    # ========================================================
    # MAXIMUM
    # ========================================================

    if (
        "maximum" in question_lower
        or "maximum value" in question_lower
        or "highest" in question_lower
        or "largest" in question_lower
    ):

        numeric_columns = list(
            df.select_dtypes(
                include=["number"]
            ).columns
        )

        if selected_column is not None:

            if selected_column not in numeric_columns:

                return (
                    f"⚠️ **{selected_column}** is not "
                    f"a numeric column."
                )

            value = (
                pd.to_numeric(
                    df[selected_column],
                    errors="coerce"
                )
                .max()
            )

            return (
                f"📈 The maximum value of "
                f"**{selected_column}** is "
                f"**{value:,.2f}**."
            )

        if len(numeric_columns) == 1:

            column = numeric_columns[0]

            value = (
                pd.to_numeric(
                    df[column],
                    errors="coerce"
                )
                .max()
            )

            return (
                f"📈 The maximum value of "
                f"**{column}** is "
                f"**{value:,.2f}**."
            )

        return (
            "🔎 Please specify which numeric "
            "column you want the maximum value for."
        )

    # ========================================================
    # TOP N
    # ========================================================

    top_match = re.search(
        r"\btop\s+(\d+)",
        question_lower
    )

    if top_match:

        number = int(
            top_match.group(1)
        )

        number = max(
            1,
            min(number, 50)
        )

        numeric_columns = list(
            df.select_dtypes(
                include=["number"]
            ).columns
        )

        if selected_column is not None:

            if selected_column not in numeric_columns:

                return (
                    f"⚠️ **{selected_column}** is not "
                    f"a numeric column."
                )

            result = (
                df[[selected_column]]
                .sort_values(
                    by=selected_column,
                    ascending=False
                )
                .head(number)
            )

            return (
                f"📊 **Top {number} values of "
                f"{selected_column}:**\n\n"
                + result.to_markdown(
                    index=False
                )
            )

        if len(numeric_columns) == 1:

            column = numeric_columns[0]

            result = (
                df[[column]]
                .sort_values(
                    by=column,
                    ascending=False
                )
                .head(number)
            )

            return (
                f"📊 **Top {number} values of "
                f"{column}:**\n\n"
                + result.to_markdown(
                    index=False
                )
            )

        return (
            "🔎 Please specify a numeric column "
            f"for the top {number} values."
        )

    # ========================================================
    # DATASET SIZE
    # ========================================================

    if (
        "dataset size" in question_lower
        or "size of dataset" in question_lower
        or "about the dataset" in question_lower
    ):

        return (
            f"📊 Your dataset contains "
            f"**{len(df):,} rows** and "
            f"**{len(df.columns):,} columns**."
        )

    # ========================================================
    # FALLBACK
    # ========================================================

    return (
        "🤔 I couldn't understand that question yet.\n\n"
        "Try asking something like:\n\n"
        "- How many rows are there?\n"
        "- Are there any missing values?\n"
        "- What is the minimum Amount?\n"
        "- What is the maximum Sales?\n"
        "- What is the average Age?\n"
        "- What are the numeric columns?\n"
        "- What are the categorical columns?\n"
        "- Show me the top 10 values."
    )