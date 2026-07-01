import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Upload Data",
    page_icon="📂",
    layout="wide"
)

st.title("📂 Upload Sales Dataset")

uploaded_file = st.file_uploader(
    "Choose a CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("✅ Dataset Uploaded Successfully")

    st.subheader("Preview")

    st.dataframe(df.head(), use_container_width=True)

    st.subheader("Dataset Information")

    c1, c2, c3 = st.columns(3)

    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing Values", int(df.isnull().sum().sum()))

    st.subheader("Column Names")

    st.write(df.columns.tolist())

    csv = df.to_csv(index=False)

    st.download_button(
        "📥 Download Uploaded Dataset",
        csv,
        "uploaded_dataset.csv",
        "text/csv"
    )

else:
    st.info("Upload a CSV file to begin.")