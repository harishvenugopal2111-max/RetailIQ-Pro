import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO

st.set_page_config(
    page_title="Report Generator",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Report Generator")

# ----------------------------
# Load Dataset
# ----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/clean_superstore.csv")

df = load_data()

st.success("Dataset Loaded Successfully")

# ----------------------------
# Preview
# ----------------------------
st.subheader("Dataset Preview")
st.dataframe(df.head(), use_container_width=True)

# ----------------------------
# KPIs
# ----------------------------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = len(df)
total_quantity = df["Quantity"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Sales", f"${total_sales:,.2f}")
c2.metric("Total Profit", f"${total_profit:,.2f}")
c3.metric("Orders", total_orders)
c4.metric("Quantity", int(total_quantity))

st.divider()

# ----------------------------
# CSV Download
# ----------------------------
csv = df.to_csv(index=False)

st.download_button(
    "📥 Download CSV",
    csv,
    "RetailIQ_Report.csv",
    "text/csv"
)

# ----------------------------
# Excel Download
# ----------------------------
excel = BytesIO()

with pd.ExcelWriter(excel, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="RetailIQ")

excel.seek(0)

st.download_button(
    "📥 Download Excel",
    excel,
    "RetailIQ_Report.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ----------------------------
# PDF Generator
# ----------------------------
def create_pdf():

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", "B", 16)

    pdf.cell(0,10,"RetailIQ Business Report",ln=True)

    pdf.ln(5)

    pdf.set_font("Arial","",12)

    pdf.cell(0,10,f"Total Sales : ${total_sales:,.2f}",ln=True)
    pdf.cell(0,10,f"Total Profit : ${total_profit:,.2f}",ln=True)
    pdf.cell(0,10,f"Orders : {total_orders}",ln=True)
    pdf.cell(0,10,f"Quantity : {int(total_quantity)}",ln=True)

    return pdf.output(dest="S")

pdf_bytes = create_pdf()

st.download_button(
    "📄 Download PDF",
    bytes(pdf_bytes),
    "RetailIQ_Report.pdf",
    "application/pdf"
)

st.divider()

st.success("✅ Report Generated Successfully")