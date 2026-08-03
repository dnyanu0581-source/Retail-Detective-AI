import streamlit as st
import pandas as pd

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Retail Detective AI",
    page_icon="🛍️",
    layout="wide"
)

# ---------------------------------------------------
# Title
# ---------------------------------------------------
st.title("🛍️ Retail Detective AI")
st.markdown("### AI-Powered Business Intelligence & Decision Support System")
st.write("Upload a retail dataset to begin analysis.")

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
st.sidebar.title("📂 Dataset Upload")
uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Supported Formats**
    - CSV (.csv)
    - Excel (.xlsx)
    """
)

# ---------------------------------------------------
# Read Dataset
# ---------------------------------------------------
if uploaded_file is not None:

    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ Dataset uploaded successfully!")

        # ---------------------------------------------------
        # Dataset Preview
        # ---------------------------------------------------
        st.header("📄 Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)

        # ---------------------------------------------------
        # Dataset Summary
        # ---------------------------------------------------
        st.header("📊 Dataset Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", df.isnull().sum().sum())
        col4.metric("Duplicate Rows", df.duplicated().sum())

        # ---------------------------------------------------
        # Dataset Information
        # ---------------------------------------------------
        st.header("📋 Dataset Information")

        info_df = pd.DataFrame({
            "Column Name": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isnull().sum().values
        })

        st.dataframe(info_df, use_container_width=True)

        # ---------------------------------------------------
        # Basic Statistics
        # ---------------------------------------------------
        st.header("📈 Statistical Summary")
        st.dataframe(df.describe(), use_container_width=True)

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    st.info("👈 Please upload a retail dataset from the sidebar to begin.")