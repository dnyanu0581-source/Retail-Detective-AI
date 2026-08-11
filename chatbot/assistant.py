import pandas as pd
import re


# ============================================================
# COLUMN DETECTION
# ============================================================

def find_column_from_question(df, question):
    """
    Try to identify a dataset column mentioned in the question.

    Supports:
        customer_id
        customer id
        total-sales
        total sales
    """

    question_lower = question.lower().strip()

    # --------------------------------------------------------
    # Exact column name
    # --------------------------------------------------------

    for column in df.columns:

        column_name = str(column).lower().strip()

        if column_name in question_lower:
            return column

    # --------------------------------------------------------
    # Normalized column name
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
    # Column words
    # Example:
    # "total sales" -> total + sales
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
# FIND NUMERIC COLUMNS
# ============================================================

def get_numeric_columns(df):

    return list(
        df.select_dtypes(
            include=["number"]
        ).columns
    )


# ============================================================
# FIND CATEGORICAL COLUMNS
# ============================================================

def get_categorical_columns(df):

    return list(
        df.select_dtypes(
            include=["object", "category", "string"]
        ).columns
    )


# ============================================================
# FORMAT NUMBER
# ============================================================

def format_number(value):

    if pd.isna(value):
        return "N/A"

    try:

        if float(value).is_integer():

            return f"{int(value):,}"

        return f"{float(value):,.2f}"

    except (ValueError, TypeError):

        return str(value)


# ============================================================
# FIND TOP / BOTTOM N
# ============================================================

def extract_n(question, default=5):

    match = re.search(
        r"\b(?:top|bottom|highest|lowest)\s+(\d+)",
        question.lower()
    )

    if match:

        number = int(match.group(1))

        return max(
            1,
            min(number, 50)
        )

    return default


# ============================================================
# ANSWER QUESTION
# ============================================================

def answer_question(df, question):
    """
    Analyze a Pandas DataFrame and answer
    natural-language questions.

    Supported operations:

    - Row count
    - Column count
    - Column names
    - Missing values
    - Duplicate rows
    - Numeric columns
    - Categorical columns
    - Unique values
    - Average / mean
    - Median
    - Minimum
    - Maximum
    - Sum / total
    - Top N
    - Bottom N
    - Dataset size
    - Grouped sum
    - Grouped average
    """

    # ========================================================
    # VALIDATION
    # ========================================================

    if df is None:

        return "❌ No dataset is available."

    if df.empty:

        return "❌ The dataset is empty."

    if not isinstance(question, str):

        return "❌ Please enter a valid question."

    question = question.strip()

    if not question:

        return "❌ Please enter a question."

    question_lower = question.lower()

    # ========================================================
    # DATASET SIZE
    # ========================================================

    if (
        "dataset size" in question_lower
        or "size of dataset" in question_lower
        or "about the dataset" in question_lower
        or "dataset information" in question_lower
    ):

        return (
            f"📊 Your dataset contains "
            f"**{len(df):,} rows** and "
            f"**{len(df.columns):,} columns**."
        )

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
        or "how many entries" in question_lower
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

        numeric_columns = get_numeric_columns(df)

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

        categorical_columns = get_categorical_columns(df)

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

    numeric_columns = get_numeric_columns(df)

    categorical_columns = get_categorical_columns(df)

    # ========================================================
    # SUM / TOTAL
    # ========================================================

    if (
        "total" in question_lower
        or "sum" in question_lower
        or "total amount" in question_lower
        or "total sales" in question_lower
        or "total revenue" in question_lower
    ):

        if selected_column is not None:

            if selected_column not in numeric_columns:

                return (
                    f"⚠️ **{selected_column}** is not "
                    f"a numeric column, so a total "
                    f"cannot be calculated."
                )

            numeric_series = pd.to_numeric(
                df[selected_column],
                errors="coerce"
            )

            value = numeric_series.sum()

            return (
                f"💰 The total of "
                f"**{selected_column}** is "
                f"**{format_number(value)}**."
            )

        if len(numeric_columns) == 1:

            column = numeric_columns[0]

            value = pd.to_numeric(
                df[column],
                errors="coerce"
            ).sum()

            return (
                f"💰 The total of "
                f"**{column}** is "
                f"**{format_number(value)}**."
            )

        return (
            "🔎 Please specify a numeric column "
            "for the total.\n\n"
            "Example: **What is the total Sales?**"
        )

    # ========================================================
    # AVERAGE / MEAN
    # ========================================================

    if (
        "average" in question_lower
        or "mean" in question_lower
    ):

        if selected_column is not None:

            if selected_column not in numeric_columns:

                return (
                    f"⚠️ **{selected_column}** is not "
                    f"a numeric column, so an average "
                    f"cannot be calculated."
                )

            value = pd.to_numeric(
                df[selected_column],
                errors="coerce"
            ).mean()

            return (
                f"📊 The average of "
                f"**{selected_column}** is "
                f"**{format_number(value)}**."
            )

        if len(numeric_columns) == 1:

            column = numeric_columns[0]

            value = pd.to_numeric(
                df[column],
                errors="coerce"
            ).mean()

            return (
                f"📊 The average of "
                f"**{column}** is "
                f"**{format_number(value)}**."
            )

        return (
            "🔎 Please specify a numeric column "
            "for the average."
        )

    # ========================================================
    # MEDIAN
    # ========================================================

    if "median" in question_lower:

        if selected_column is not None:

            if selected_column not in numeric_columns:

                return (
                    f"⚠️ **{selected_column}** is not "
                    f"a numeric column."
                )

            value = pd.to_numeric(
                df[selected_column],
                errors="coerce"
            ).median()

            return (
                f"📊 The median of "
                f"**{selected_column}** is "
                f"**{format_number(value)}**."
            )

        if len(numeric_columns) == 1:

            column = numeric_columns[0]

            value = pd.to_numeric(
                df[column],
                errors="coerce"
            ).median()

            return (
                f"📊 The median of "
                f"**{column}** is "
                f"**{format_number(value)}**."
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

        if selected_column is not None:

            if selected_column not in numeric_columns:

                return (
                    f"⚠️ **{selected_column}** is not "
                    f"a numeric column."
                )

            value = pd.to_numeric(
                df[selected_column],
                errors="coerce"
            ).min()

            return (
                f"📉 The minimum value of "
                f"**{selected_column}** is "
                f"**{format_number(value)}**."
            )

        if len(numeric_columns) == 1:

            column = numeric_columns[0]

            value = pd.to_numeric(
                df[column],
                errors="coerce"
            ).min()

            return (
                f"📉 The minimum value of "
                f"**{column}** is "
                f"**{format_number(value)}**."
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

        if selected_column is not None:

            if selected_column not in numeric_columns:

                return (
                    f"⚠️ **{selected_column}** is not "
                    f"a numeric column."
                )

            value = pd.to_numeric(
                df[selected_column],
                errors="coerce"
            ).max()

            return (
                f"📈 The maximum value of "
                f"**{selected_column}** is "
                f"**{format_number(value)}**."
            )

        if len(numeric_columns) == 1:

            column = numeric_columns[0]

            value = pd.to_numeric(
                df[column],
                errors="coerce"
            ).max()

            return (
                f"📈 The maximum value of "
                f"**{column}** is "
                f"**{format_number(value)}**."
            )

        return (
            "🔎 Please specify which numeric "
            "column you want the maximum value for."
        )

    # ========================================================
    # TOP N
    # ========================================================

    if (
        "top " in question_lower
        or "highest " in question_lower
    ):

        number = extract_n(
            question,
            default=5
        )

        if selected_column is not None:

            if selected_column not in numeric_columns:

                return (
                    f"⚠️ **{selected_column}** is not "
                    f"a numeric column."
                )

            result = (
                df[[selected_column]]
                .copy()
            )

            result[selected_column] = pd.to_numeric(
                result[selected_column],
                errors="coerce"
            )

            result = (
                result
                .dropna()
                .sort_values(
                    by=selected_column,
                    ascending=False
                )
                .head(number)
            )

            if result.empty:

                return (
                    f"❌ No usable numeric values "
                    f"were found in **{selected_column}**."
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
                .copy()
            )

            result[column] = pd.to_numeric(
                result[column],
                errors="coerce"
            )

            result = (
                result
                .dropna()
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
            f"🔎 Please specify a numeric column "
            f"for the top {number} values.\n\n"
            f"Example: **Show the top 5 Sales.**"
        )

    # ========================================================
    # BOTTOM N
    # ========================================================

    if (
        "bottom " in question_lower
        or "lowest " in question_lower
    ):

        number = extract_n(
            question,
            default=5
        )

        if selected_column is not None:

            if selected_column not in numeric_columns:

                return (
                    f"⚠️ **{selected_column}** is not "
                    f"a numeric column."
                )

            result = (
                df[[selected_column]]
                .copy()
            )

            result[selected_column] = pd.to_numeric(
                result[selected_column],
                errors="coerce"
            )

            result = (
                result
                .dropna()
                .sort_values(
                    by=selected_column,
                    ascending=True
                )
                .head(number)
            )

            return (
                f"📉 **Bottom {number} values of "
                f"{selected_column}:**\n\n"
                + result.to_markdown(
                    index=False
                )
            )

        if len(numeric_columns) == 1:

            column = numeric_columns[0]

            result = (
                df[[column]]
                .copy()
            )

            result[column] = pd.to_numeric(
                result[column],
                errors="coerce"
            )

            result = (
                result
                .dropna()
                .sort_values(
                    by=column,
                    ascending=True
                )
                .head(number)
            )

            return (
                f"📉 **Bottom {number} values of "
                f"{column}:**\n\n"
                + result.to_markdown(
                    index=False
                )
            )

        return (
            f"🔎 Please specify a numeric column "
            f"for the bottom {number} values."
        )

    # ========================================================
    # GROUPED SUM
    # Example:
    # total sales by region
    # sales by category
    # revenue by product
    # ========================================================

    if (
        " by " in question_lower
        and (
            "total" in question_lower
            or "sum" in question_lower
        )
    ):

        numeric_column = selected_column

        if numeric_column is None:

            if len(numeric_columns) == 1:

                numeric_column = numeric_columns[0]

            else:

                return (
                    "🔎 Please specify the numeric "
                    "column you want to summarize."
                )

        if numeric_column not in numeric_columns:

            return (
                f"⚠️ **{numeric_column}** is not "
                f"a numeric column."
            )

        # Find categorical column after "by"
        by_match = re.search(
            r"\bby\s+(.+)",
            question_lower
        )

        group_column = None

        if by_match:

            group_text = (
                by_match
                .group(1)
                .strip()
                .rstrip("?")
            )

            group_column = find_column_from_question(
                df,
                group_text
            )

        if group_column is None:

            if len(categorical_columns) == 1:

                group_column = categorical_columns[0]

            else:

                return (
                    "🔎 Please specify a category "
                    "to group the data by.\n\n"
                    "Example: **Total Sales by Region**"
                )

        result = (
            df.groupby(
                group_column,
                dropna=False
            )[numeric_column]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(20)
            .reset_index()
        )

        result.columns = [
            group_column,
            f"Total {numeric_column}"
        ]

        return (
            f"📊 **Total {numeric_column} by "
            f"{group_column}:**\n\n"
            + result.to_markdown(
                index=False
            )
        )

    # ========================================================
    # GROUPED AVERAGE
    # Example:
    # average sales by region
    # average amount by category
    # ========================================================

    if (
        " by " in question_lower
        and (
            "average" in question_lower
            or "mean" in question_lower
        )
    ):

        numeric_column = selected_column

        if numeric_column is None:

            if len(numeric_columns) == 1:

                numeric_column = numeric_columns[0]

            else:

                return (
                    "🔎 Please specify the numeric "
                    "column you want to average."
                )

        if numeric_column not in numeric_columns:

            return (
                f"⚠️ **{numeric_column}** is not "
                f"a numeric column."
            )

        by_match = re.search(
            r"\bby\s+(.+)",
            question_lower
        )

        group_column = None

        if by_match:

            group_text = (
                by_match
                .group(1)
                .strip()
                .rstrip("?")
            )

            group_column = find_column_from_question(
                df,
                group_text
            )

        if group_column is None:

            if len(categorical_columns) == 1:

                group_column = categorical_columns[0]

            else:

                return (
                    "🔎 Please specify a category "
                    "to group the data by.\n\n"
                    "Example: **Average Sales by Region**"
                )

        result = (
            df.groupby(
                group_column,
                dropna=False
            )[numeric_column]
            .mean()
            .sort_values(
                ascending=False
            )
            .head(20)
            .reset_index()
        )

        result.columns = [
            group_column,
            f"Average {numeric_column}"
        ]

        return (
            f"📊 **Average {numeric_column} by "
            f"{group_column}:**\n\n"
            + result.to_markdown(
                index=False
            )
        )

    # ========================================================
    # COLUMN VALUE COUNTS
    # ========================================================

    if (
        "most common" in question_lower
        or "most frequent" in question_lower
        or "popular" in question_lower
    ):

        if selected_column is None:

            if len(categorical_columns) == 1:

                selected_column = categorical_columns[0]

            else:

                return (
                    "🔎 Please specify a column "
                    "to find the most common values."
                )

        counts = (
            df[selected_column]
            .fillna("Missing")
            .astype(str)
            .value_counts()
            .head(10)
        )

        result = pd.DataFrame({
            selected_column: counts.index,
            "Count": counts.values
        })

        return (
            f"🔤 **Most common values in "
            f"{selected_column}:**\n\n"
            + result.to_markdown(
                index=False
            )
        )

    # ========================================================
    # FALLBACK
    # ========================================================

    return (
        "🤔 I couldn't understand that question yet.\n\n"
        "### Try asking:\n\n"
        "- How many rows are there?\n"
        "- How many columns are there?\n"
        "- Are there any missing values?\n"
        "- How many duplicate rows are there?\n"
        "- What are the numeric columns?\n"
        "- What are the categorical columns?\n"
        "- What is the average Sales?\n"
        "- What is the median Age?\n"
        "- What is the minimum Amount?\n"
        "- What is the maximum Sales?\n"
        "- What is the total Revenue?\n"
        "- Show the top 5 Sales.\n"
        "- Show the bottom 5 Sales.\n"
        "- What is the total Sales by Region?\n"
        "- What is the average Sales by Category?\n"
        "- What are the most common Products?"
    )
