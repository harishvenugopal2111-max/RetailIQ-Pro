import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/clean_superstore.csv")

    # Safe Date Conversion
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce",
        format="mixed"
    )

    df = df.dropna(subset=["Order Date"])

    return df

df = load_data()

# ---------------- TITLE ----------------
st.title("📈 RetailIQ Analytics")

# ---------------- FILTER ----------------
category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["Category"].unique().tolist())
)

if category != "All":
    df = df[df["Category"] == category]

# ---------------- KPIs ----------------
c1, c2, c3 = st.columns(3)

c1.metric("Total Sales", f"${df['Sales'].sum():,.2f}")
c2.metric("Total Profit", f"${df['Profit'].sum():,.2f}")
c3.metric("Orders", len(df))

st.divider()

# ---------------- MONTHLY SALES ----------------
monthly = (
    df.groupby(df["Order Date"].dt.strftime("%Y-%m"))["Sales"]
    .sum()
    .reset_index()
)

fig = px.line(
    monthly,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- CATEGORY SALES ----------------
category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Category"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- STATE SALES ----------------
state_sales = (
    df.groupby("State")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    state_sales,
    x="State",
    y="Sales",
    color="Sales",
    text_auto=".2s"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- REGION ----------------
region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig = px.pie(
    region_sales,
    names="Region",
    values="Sales",
    hole=0.5
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- TOP PRODUCTS ----------------
st.subheader("🏆 Top 10 Products")

products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(products)

st.success("✅ Analytics Loaded Successfully")