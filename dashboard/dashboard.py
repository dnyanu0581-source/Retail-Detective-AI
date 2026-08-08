import streamlit as st
import pandas as pd
import io


# ============================================================
# LOGOUT
# ============================================================

def logout():

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.email = None

    # Remove working datasets
    for key in [
        "dataset",
        "cleaned_dataset",
        "dataset_name"
    ]:
        if key in st.session_state:
            del st.session_state[key]

    st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard():

    # ========================================================
    # SIDEBAR
    # ========================================================

    st.sidebar.title("🛍️ Retail Detective AI")

    st.sidebar.markdown("---")

    st.sidebar.write("👤 **Logged in as:**")

    st.sidebar.write(
        st.session_state.get("username", "User")
    )

    st.sidebar.markdown("---")

    st.sidebar.subheader("Navigation")

    page = st.sidebar.radio(
        "Go to",
        [
            "🏠 Dashboard",
            "📂 Dataset",
            "📈 Analytics",
            "🧹 Data Cleaning",
            "🤖 AI Assistant",
            "📑 Reports"
        ]
    )

    st.sidebar.markdown("---")

    if st.sidebar.button(
        "🚪 Logout",
        width="stretch"
    ):
        logout()


    # ========================================================
    # DASHBOARD HOME
    # ========================================================

    if page == "🏠 Dashboard":

        st.title("🛍️ Retail Detective AI")

        st.success(
            f"Welcome, "
            f"{st.session_state.get('username', 'User')}! 👋"
        )

        st.subheader(
            "AI-Powered Business Intelligence & "
            "Decision Support System"
        )

        st.write(
            "Upload a dataset and use Retail Detective AI "
            "to clean, analyze and understand your data."
        )

        st.markdown("---")

        if "dataset" in st.session_state:

            df = st.session_state.dataset

            st.subheader("📊 Current Dataset")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Rows",
                f"{len(df):,}"
            )

            col2.metric(
                "Columns",
                len(df.columns)
            )

            col3.metric(
                "Missing Values",
                f"{int(df.isnull().sum().sum()):,}"
            )

            col4.metric(
                "Duplicate Rows",
                f"{int(df.duplicated().sum()):,}"
            )

            st.success(
                "✅ Dataset is loaded and ready."
            )

        else:

            st.info(
                "👈 Go to **📂 Dataset** and upload "
                "a CSV or Excel file."
            )


    # ========================================================
    # DATASET
    # ========================================================

    elif page == "📂 Dataset":

        st.title("📂 Dataset")

        st.write(
            "Upload any CSV or Excel dataset."
        )

        uploaded_file = st.file_uploader(
            "Choose a dataset",
            type=["csv", "xlsx"]
        )

        if uploaded_file is not None:

            try:

                if uploaded_file.name.lower().endswith(".csv"):

                    df = pd.read_csv(uploaded_file)

                else:

                    df = pd.read_excel(uploaded_file)

                # Store original dataset
                st.session_state.dataset = df.copy()

                st.session_state.dataset_name = (
                    uploaded_file.name
                )

                # Remove old cleaned dataset
                if "cleaned_dataset" in st.session_state:

                    del st.session_state.cleaned_dataset

                st.success(
                    "✅ Dataset uploaded successfully!"
                )

                st.info(
                    f"📄 File: {uploaded_file.name}"
                )

                st.markdown("---")

                # ------------------------------------------------
                # PREVIEW
                # ------------------------------------------------

                st.subheader("📄 Dataset Preview")

                preview_rows = st.selectbox(
                    "Number of rows to preview",
                    [10, 25, 50, 100],
                    index=0,
                    key="dataset_preview_rows"
                )

                st.dataframe(
                    df.head(preview_rows),
                    width="stretch"
                )

                st.markdown("---")

                # ------------------------------------------------
                # SUMMARY
                # ------------------------------------------------

                st.subheader("📊 Dataset Summary")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Rows",
                    f"{len(df):,}"
                )

                col2.metric(
                    "Columns",
                    len(df.columns)
                )

                col3.metric(
                    "Missing Values",
                    f"{int(df.isnull().sum().sum()):,}"
                )

                col4.metric(
                    "Duplicate Rows",
                    f"{int(df.duplicated().sum()):,}"
                )

                st.markdown("---")

                # ------------------------------------------------
                # INFORMATION
                # ------------------------------------------------

                st.subheader("📋 Dataset Information")

                info_df = pd.DataFrame({
                    "Column Name": df.columns,
                    "Data Type": df.dtypes.astype(str).values,
                    "Missing Values": (
                        df.isnull().sum().values
                    ),
                    "Unique Values": [
                        df[column].nunique(
                            dropna=True
                        )
                        for column in df.columns
                    ]
                })

                st.dataframe(
                    info_df,
                    width="stretch"
                )

                st.markdown("---")

                # ------------------------------------------------
                # STATISTICS
                # ------------------------------------------------

                st.subheader("📈 Statistical Summary")

                numeric_df = df.select_dtypes(
                    include=["number"]
                )

                if not numeric_df.empty:

                    st.dataframe(
                        numeric_df.describe(),
                        width="stretch"
                    )

                else:

                    st.info(
                        "No numeric columns found."
                    )

            except Exception as e:

                st.error(
                    f"❌ Error reading dataset: {e}"
                )

        elif "dataset" in st.session_state:

            st.success(
                "✅ Dataset is already loaded."
            )

            st.write(
                f"Current file: "
                f"**{st.session_state.get('dataset_name', 'Dataset')}**"
            )

        else:

            st.info(
                "👈 Upload a CSV or Excel file to begin."
            )


    # ========================================================
    # DATA CLEANING
    # ========================================================

    elif page == "🧹 Data Cleaning":

        st.title("🧹 Data Cleaning")

        st.write(
            """
            Analyze and clean your dataset without modifying
            the original uploaded data.
            """
        )

        if "dataset" not in st.session_state:

            st.warning(
                "⚠️ Please upload a dataset first."
            )

        else:

            original_df = (
                st.session_state.dataset.copy()
            )

            if "cleaned_dataset" not in st.session_state:

                st.session_state.cleaned_dataset = (
                    original_df.copy()
                )

            df = (
                st.session_state.cleaned_dataset.copy()
            )

            # =================================================
            # CURRENT STATUS
            # =================================================

            st.subheader("📊 Current Dataset Status")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Rows",
                f"{len(df):,}"
            )

            col2.metric(
                "Columns",
                len(df.columns)
            )

            col3.metric(
                "Missing Values",
                f"{int(df.isnull().sum().sum()):,}"
            )

            col4.metric(
                "Duplicate Rows",
                f"{int(df.duplicated().sum()):,}"
            )

            # =================================================
            # MISSING VALUES
            # =================================================

            st.markdown("---")

            st.subheader("🔍 Missing Value Analysis")

            missing_df = pd.DataFrame({
                "Column": df.columns,
                "Missing Values": (
                    df.isnull().sum().values
                ),
                "Missing %": (
                    df.isnull().mean().values * 100
                ).round(2)
            })

            missing_columns = missing_df[
                missing_df["Missing Values"] > 0
            ]

            if missing_columns.empty:

                st.success(
                    "✅ No missing values detected."
                )

            else:

                st.dataframe(
                    missing_columns,
                    width="stretch"
                )

            # =================================================
            # DUPLICATES
            # =================================================

            st.markdown("---")

            st.subheader("🔁 Duplicate Analysis")

            duplicate_count = int(
                df.duplicated().sum()
            )

            if duplicate_count == 0:

                st.success(
                    "✅ No duplicate rows detected."
                )

            else:

                st.warning(
                    f"⚠️ {duplicate_count:,} "
                    "duplicate rows detected."
                )

            # =================================================
            # CLEANING OPTIONS
            # =================================================

            st.markdown("---")

            st.subheader("🛠️ Cleaning Options")

            remove_duplicates = st.checkbox(
                "🗑️ Remove duplicate rows",
                value=False,
                key="remove_duplicates"
            )

            missing_method = st.selectbox(
                "🩹 Missing value handling",
                [
                    "Do not change missing values",
                    "Remove rows containing missing values",
                    "Fill numeric values with mean",
                    "Fill numeric values with median",
                    "Fill missing values with mode"
                ],
                key="missing_method"
            )

            if st.button(
                "🧹 Apply Cleaning",
                type="primary",
                width="stretch"
            ):

                cleaned_df = df.copy()

                # Remove duplicates
                if remove_duplicates:

                    cleaned_df = (
                        cleaned_df
                        .drop_duplicates()
                        .reset_index(drop=True)
                    )

                # Remove missing rows
                if missing_method == (
                    "Remove rows containing missing values"
                ):

                    cleaned_df = (
                        cleaned_df
                        .dropna()
                        .reset_index(drop=True)
                    )

                # Mean
                elif missing_method == (
                    "Fill numeric values with mean"
                ):

                    numeric_columns = (
                        cleaned_df
                        .select_dtypes(
                            include=["number"]
                        )
                        .columns
                    )

                    for column in numeric_columns:

                        if cleaned_df[column].isnull().any():

                            mean_value = (
                                cleaned_df[column].mean()
                            )

                            cleaned_df[column] = (
                                cleaned_df[column]
                                .fillna(mean_value)
                            )

                # Median
                elif missing_method == (
                    "Fill numeric values with median"
                ):

                    numeric_columns = (
                        cleaned_df
                        .select_dtypes(
                            include=["number"]
                        )
                        .columns
                    )

                    for column in numeric_columns:

                        if cleaned_df[column].isnull().any():

                            median_value = (
                                cleaned_df[column].median()
                            )

                            cleaned_df[column] = (
                                cleaned_df[column]
                                .fillna(median_value)
                            )

                # Mode
                elif missing_method == (
                    "Fill missing values with mode"
                ):

                    for column in cleaned_df.columns:

                        if cleaned_df[column].isnull().any():

                            mode_values = (
                                cleaned_df[column].mode()
                            )

                            if not mode_values.empty:

                                cleaned_df[column] = (
                                    cleaned_df[column]
                                    .fillna(
                                        mode_values.iloc[0]
                                    )
                                )

                st.session_state.cleaned_dataset = (
                    cleaned_df.copy()
                )

                st.success(
                    "✅ Cleaning applied successfully!"
                )

                st.rerun()

            # =================================================
            # BEFORE / AFTER
            # =================================================

            st.markdown("---")

            st.subheader(
                "📊 Before vs After Cleaning"
            )

            comparison_df = pd.DataFrame({
                "Metric": [
                    "Rows",
                    "Missing Values",
                    "Duplicate Rows"
                ],
                "Original": [
                    len(original_df),
                    int(
                        original_df.isnull()
                        .sum()
                        .sum()
                    ),
                    int(
                        original_df.duplicated()
                        .sum()
                    )
                ],
                "Cleaned": [
                    len(df),
                    int(
                        df.isnull()
                        .sum()
                        .sum()
                    ),
                    int(
                        df.duplicated()
                        .sum()
                    )
                ]
            })

            st.dataframe(
                comparison_df,
                width="stretch"
            )

            # =================================================
            # PREVIEW
            # =================================================

            st.markdown("---")

            st.subheader(
                "📄 Cleaned Dataset Preview"
            )

            st.dataframe(
                df.head(20),
                width="stretch"
            )

            # =================================================
            # DOWNLOAD
            # =================================================

            st.markdown("---")

            st.subheader(
                "💾 Download Cleaned Dataset"
            )

            csv_buffer = io.StringIO()

            df.to_csv(
                csv_buffer,
                index=False
            )

            st.download_button(
                label="⬇️ Download Cleaned CSV",
                data=csv_buffer.getvalue(),
                file_name="cleaned_dataset.csv",
                mime="text/csv",
                width="stretch"
            )

            # =================================================
            # RESET
            # =================================================

            st.markdown("---")

            if st.button(
                "🔄 Reset to Original Dataset",
                width="stretch"
            ):

                st.session_state.cleaned_dataset = (
                    original_df.copy()
                )

                st.success(
                    "✅ Dataset restored."
                )

                st.rerun()


    # ========================================================
    # ANALYTICS
    # ========================================================

    elif page == "📈 Analytics":

        st.title("📈 Analytics")

        st.write(
            "Automatically explore and visualize "
            "your uploaded dataset."
        )

        if "dataset" not in st.session_state:

            st.warning(
                "⚠️ Please upload a dataset first "
                "from the 📂 Dataset section."
            )

        else:

            # Use cleaned dataset if available
            if "cleaned_dataset" in st.session_state:

                df = (
                    st.session_state.cleaned_dataset
                    .copy()
                )

                st.success(
                    "✅ Using the cleaned dataset for analysis."
                )

            else:

                df = (
                    st.session_state.dataset
                    .copy()
                )

                st.info(
                    "ℹ️ Using the original dataset."
                )

            # =================================================
            # COLUMN TYPES
            # =================================================

            numeric_columns = list(
                df.select_dtypes(
                    include=["number"]
                ).columns
            )

            categorical_columns = list(
                df.select_dtypes(
                    include=["object", "category"]
                ).columns
            )

            # =================================================
            # OVERVIEW
            # =================================================

            st.markdown("---")

            st.subheader("📊 Dataset Overview")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Rows",
                f"{len(df):,}"
            )

            col2.metric(
                "Columns",
                len(df.columns)
            )

            col3.metric(
                "Numeric Columns",
                len(numeric_columns)
            )

            col4.metric(
                "Text Columns",
                len(categorical_columns)
            )

            # =================================================
            # COLUMN INFORMATION
            # =================================================

            st.markdown("---")

            st.subheader("🔤 Column Information")

            column_info = pd.DataFrame({
                "Column": df.columns,
                "Data Type": df.dtypes.astype(str).values,
                "Unique Values": [
                    df[column].nunique(
                        dropna=True
                    )
                    for column in df.columns
                ],
                "Missing Values": [
                    int(
                        df[column].isnull().sum()
                    )
                    for column in df.columns
                ]
            })

            st.dataframe(
                column_info,
                width="stretch"
            )

            # =================================================
            # NUMERIC ANALYSIS
            # =================================================

            st.markdown("---")

            st.subheader("🔢 Numeric Analysis")

            if not numeric_columns:

                st.info(
                    "No numeric columns were detected."
                )

            else:

                selected_numeric = st.selectbox(
                    "Select a numeric column",
                    numeric_columns,
                    key="analytics_numeric_column"
                )

                numeric_series = (
                    pd.to_numeric(
                        df[selected_numeric],
                        errors="coerce"
                    )
                    .dropna()
                )

                if numeric_series.empty:

                    st.warning(
                        "This column contains no usable "
                        "numeric values."
                    )

                else:

                    col1, col2, col3, col4 = st.columns(4)

                    col1.metric(
                        "Minimum",
                        f"{numeric_series.min():,.2f}"
                    )

                    col2.metric(
                        "Maximum",
                        f"{numeric_series.max():,.2f}"
                    )

                    col3.metric(
                        "Average",
                        f"{numeric_series.mean():,.2f}"
                    )

                    col4.metric(
                        "Median",
                        f"{numeric_series.median():,.2f}"
                    )

                    st.subheader(
                        f"📊 Statistics: {selected_numeric}"
                    )

                    statistics = (
                        numeric_series.describe()
                    )

                    statistics_df = pd.DataFrame({
                        "Statistic": statistics.index,
                        "Value": statistics.values
                    })

                    st.dataframe(
                        statistics_df,
                        width="stretch"
                    )

                    # -----------------------------------------
                    # HISTOGRAM
                    # -----------------------------------------

                    st.subheader(
                        f"📈 Distribution: {selected_numeric}"
                    )

                    try:

                        histogram_counts, histogram_bins = (
                            pd.cut(
                                numeric_series,
                                bins=10,
                                retbins=True
                            )
                        )

                        histogram_data = (
                            histogram_counts
                            .value_counts()
                            .sort_index()
                        )

                        histogram_df = pd.DataFrame({
                            "Range": (
                                histogram_data
                                .index
                                .astype(str)
                            ),
                            "Count": (
                                histogram_data.values
                            )
                        })

                        st.bar_chart(
                            histogram_df.set_index(
                                "Range"
                            )
                        )

                    except Exception:

                        st.info(
                            "Unable to create distribution "
                            "chart for this column."
                        )

            # =================================================
            # CATEGORICAL ANALYSIS
            # =================================================

            st.markdown("---")

            st.subheader(
                "🔤 Categorical Analysis"
            )

            if not categorical_columns:

                st.info(
                    "No categorical/text columns detected."
                )

            else:

                selected_category = st.selectbox(
                    "Select a categorical column",
                    categorical_columns,
                    key="analytics_category_column"
                )

                category_counts = (
                    df[selected_category]
                    .fillna("Missing")
                    .astype(str)
                    .value_counts()
                    .head(20)
                )

                st.subheader(
                    f"📊 Top Values: "
                    f"{selected_category}"
                )

                category_df = pd.DataFrame({
                    "Value": category_counts.index,
                    "Count": category_counts.values
                })

                st.dataframe(
                    category_df,
                    width="stretch"
                )

                st.subheader(
                    f"📈 Distribution: "
                    f"{selected_category}"
                )

                st.bar_chart(
                    category_df.set_index("Value")
                )

            # =================================================
            # CORRELATION
            # =================================================

            st.markdown("---")

            st.subheader(
                "🔗 Correlation Analysis"
            )

            if len(numeric_columns) < 2:

                st.info(
                    "At least two numeric columns are "
                    "required for correlation analysis."
                )

            else:

                correlation_matrix = (
                    df[numeric_columns]
                    .corr()
                )

                st.dataframe(
                    correlation_matrix.round(2),
                    width="stretch"
                )

                st.write(
                    """
                    **Correlation interpretation:**

                    • Close to **+1** → strong positive relationship

                    • Close to **-1** → strong negative relationship

                    • Close to **0** → weak or no linear relationship
                    """
                )

            # =================================================
            # COLUMN EXPLORER
            # =================================================

            st.markdown("---")

            st.subheader(
                "🔎 Column Explorer"
            )

            selected_column = st.selectbox(
                "Choose any column",
                list(df.columns),
                key="analytics_column_explorer"
            )

            selected_data = df[selected_column]

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Data Type",
                str(selected_data.dtype)
            )

            col2.metric(
                "Unique Values",
                f"{selected_data.nunique(dropna=True):,}"
            )

            col3.metric(
                "Missing Values",
                f"{int(selected_data.isnull().sum()):,}"
            )

            st.write(
                f"### 📄 Values in `{selected_column}`"
            )

            explorer_df = (
                selected_data
                .fillna("Missing")
                .astype(str)
                .value_counts()
                .head(20)
                .rename("Count")
                .to_frame()
            )

            st.dataframe(
                explorer_df,
                width="stretch"
            )

            # =================================================
            # DATA PREVIEW
            # =================================================

            st.markdown("---")

            st.subheader(
                "📄 Dataset Preview"
            )

            analytics_preview_rows = st.selectbox(
                "Rows to display",
                [10, 25, 50, 100],
                key="analytics_preview_rows"
            )

            st.dataframe(
                df.head(analytics_preview_rows),
                width="stretch"
            )


    # ========================================================
    # AI ASSISTANT
    # ========================================================

    elif page == "🤖 AI Assistant":

        st.title("🤖 Retail Detective AI Assistant")

        st.write(
            "Ask questions about your uploaded dataset "
            "using natural language."
        )

        if "dataset" not in st.session_state:

            st.warning("⚠️ Please upload a dataset first.")

        else:

            try:
                from chatbot.assistant import answer_question
            except ImportError as e:
                st.error("❌ Could not load the AI Assistant.")
                st.code(str(e))
            else:

                if "cleaned_dataset" in st.session_state:
                    df = st.session_state.cleaned_dataset.copy()
                    st.success(
                        "✅ AI Assistant is using your cleaned dataset."
                    )
                else:
                    df = st.session_state.dataset.copy()
                    st.info(
                        "ℹ️ AI Assistant is using your uploaded dataset."
                    )

                col1, col2, col3 = st.columns(3)
                col1.metric("Rows", f"{len(df):,}")
                col2.metric("Columns", len(df.columns))
                col3.metric(
                    "Missing Values",
                    f"{int(df.isnull().sum().sum()):,}"
                )

                st.markdown("---")
                st.subheader("💬 Ask Your Dataset")

                question = st.text_input(
                    "Type your question",
                    placeholder="Example: What is the minimum Amount?",
                    key="ai_question"
                )

                if st.button(
                    "🤖 Ask AI",
                    type="primary",
                    width="stretch",
                    key="ask_ai_button"
                ):

                    if not question.strip():
                        st.warning("⚠️ Please enter a question.")
                    else:
                        st.session_state.ai_pending_question = question.strip()
                        st.session_state.ai_show_column_selector = True
                        st.rerun()

                if st.session_state.get("ai_show_column_selector", False):

                    pending_question = st.session_state.get(
                        "ai_pending_question", ""
                    )
                    question_lower = pending_question.lower()

                    column_required = any(
                        keyword in question_lower
                        for keyword in [
                            "minimum", "maximum", "highest",
                            "lowest", "smallest", "largest",
                            "average", "mean", "median", "top "
                        ]
                    )

                    detected_column = None

                    for column in df.columns:
                        column_name = str(column).lower().strip()
                        normalized_name = (
                            column_name
                            .replace("_", " ")
                            .replace("-", " ")
                        )

                        if (
                            column_name in question_lower
                            or normalized_name in question_lower
                        ):
                            detected_column = column
                            break

                    if detected_column is not None or not column_required:

                        with st.spinner("🔎 Analyzing your dataset..."):
                            try:
                                answer = answer_question(
                                    df, pending_question
                                )
                                st.markdown("---")
                                st.subheader("🤖 Answer")
                                st.markdown(answer)
                            except Exception as e:
                                st.error(
                                    f"❌ Error analyzing dataset: {e}"
                                )

                        st.session_state.ai_show_column_selector = False

                    else:

                        numeric_columns = list(
                            df.select_dtypes(
                                include=["number"]
                            ).columns
                        )

                        if not numeric_columns:

                            st.warning(
                                "⚠️ No numeric columns were found "
                                "in this dataset."
                            )

                            st.session_state.ai_show_column_selector = False

                        else:

                            st.info(
                                "🔎 Your question requires a numeric "
                                "column. Select the column below."
                            )

                            selected_column = st.selectbox(
                                "Select column",
                                numeric_columns,
                                key="ai_column_selector"
                            )

                            if st.button(
                                "✅ Get Answer",
                                type="primary",
                                width="stretch",
                                key="get_ai_answer_button"
                            ):

                                final_question = (
                                    f"{pending_question} "
                                    f"for column {selected_column}"
                                )

                                with st.spinner(
                                    "🔎 Analyzing your dataset..."
                                ):
                                    try:
                                        answer = answer_question(
                                            df, final_question
                                        )

                                        st.markdown("---")
                                        st.subheader("🤖 Answer")
                                        st.markdown(answer)

                                        st.caption(
                                            f"Column analyzed: "
                                            f"**{selected_column}**"
                                        )

                                    except Exception as e:
                                        st.error(
                                            f"❌ Error analyzing dataset: {e}"
                                        )

                                st.session_state.ai_show_column_selector = False
                                st.session_state.ai_pending_question = ""

                st.markdown("---")
                st.subheader("💡 Suggested Questions")

                st.caption(
                    "These are examples only. You can type "
                    "your own question above."
                )

                suggestions = [
                    "How many rows are there?",
                    "How many columns are there?",
                    "Are there any missing values?",
                    "How many duplicate rows are there?",
                    "What are the numeric columns?",
                    "What are the categorical columns?",
                    "What is the average value?",
                    "What is the minimum value?",
                    "What is the maximum value?",
                    "Show me the top 10 values."
                ]

                for suggestion in suggestions:
                    st.markdown(f"• {suggestion}")

# ========================================================
# REPORTS
# ========================================================

    elif page == "📑 Reports":

     st.title("📑 Data Analysis Report")

    st.write(
        "Automatically generated report based on your dataset."
    )

    # Use cleaned dataset if available
    if "cleaned_dataset" in st.session_state:

        df = st.session_state.cleaned_dataset.copy()

        st.success(
            "✅ Report generated from the cleaned dataset."
        )

    elif "dataset" in st.session_state:

        df = st.session_state.dataset.copy()

        st.info(
            "ℹ️ Report generated from the uploaded dataset."
        )

    else:

        st.warning(
            "⚠️ Please upload a dataset first."
        )

        st.stop()

    # ========================================================
    # DATASET OVERVIEW
    # ========================================================

    st.header("📊 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Rows",
        f"{len(df):,}"
    )

    col2.metric(
        "Total Columns",
        f"{len(df.columns):,}"
    )

    col3.metric(
        "Missing Values",
        f"{int(df.isnull().sum().sum()):,}"
    )

    col4.metric(
        "Duplicate Rows",
        f"{int(df.duplicated().sum()):,}"
    )
    # ========================================================
    # COLUMN INFORMATION
    # ========================================================

    st.header("📋 Column Information")

    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": [
            str(dtype)
            for dtype in df.dtypes
        ],
        "Missing Values": [
            int(df[column].isnull().sum())
            for column in df.columns
        ],
        "Unique Values": [
            int(df[column].nunique())
            for column in df.columns
        ]
    })

    st.dataframe(
        column_info,
        width="stretch",
        hide_index=True
    )
    # ========================================================
    # STATISTICAL SUMMARY
    # ========================================================

    st.header("📈 Statistical Summary")

    numeric_df = df.select_dtypes(
        include=["number"]
    )

    if numeric_df.empty:

        st.info(
            "ℹ️ No numeric columns were found "
            "for statistical analysis."
        )

    else:

        summary = numeric_df.describe().T

        st.dataframe(
            summary,
            width="stretch"
        )
    # ========================================================
    # DATA QUALITY
    # ========================================================

    st.header("🔎 Data Quality")

    total_missing = int(
        df.isnull().sum().sum()
    )

    total_duplicates = int(
        df.duplicated().sum()
    )

    if total_missing == 0:

        st.success(
            "✅ No missing values detected."
        )

    else:

        st.warning(
            f"⚠️ {total_missing:,} missing values detected."
        )

    if total_duplicates == 0:

        st.success(
            "✅ No duplicate rows detected."
        )

    else:

        st.warning(
            f"⚠️ {total_duplicates:,} duplicate rows detected."
        )                
