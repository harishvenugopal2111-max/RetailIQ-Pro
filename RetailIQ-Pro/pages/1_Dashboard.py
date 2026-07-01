import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------
# PAGE CONFIG
# ------------------------------------
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------
# LOAD DATA
# ------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/clean_superstore.csv")

df = load_data()

# ------------------------------------
# PAGE TITLE
# ------------------------------------
st.title("📊 RetailIQ Pro Dashboard")
st.markdown("Welcome to your AI Powered Business Intelligence Dashboard")
st.divider()

# ------------------------------------
# SIDEBAR FILTERS
# ------------------------------------
st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

category = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

state = st.sidebar.multiselect(
    "State",
    sorted(df["State"].unique()),
    default=sorted(df["State"].unique())
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["State"].isin(state))
]

# ------------------------------------
# KPI CARDS
# ------------------------------------
sales = filtered_df["Sales"].sum()
profit = filtered_df["Profit"].sum()
orders = len(filtered_df)
quantity = filtered_df["Quantity"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Sales", f"${sales:,.2f}")
c2.metric("📈 Total Profit", f"${profit:,.2f}")
c3.metric("🛒 Orders", orders)
c4.metric("📦 Quantity", int(quantity))

st.divider()

# ------------------------------------
# SALES BY CATEGORY
# ------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("Sales by Category")

    sales_category = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        sales_category,
        x="Category",
        y="Sales",
        color="Category",
        text_auto=".2s"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Profit by Region")

    profit_region = (
        filtered_df.groupby("Region")["Profit"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        profit_region,
        names="Region",
        values="Profit",
        hole=0.5
    )

    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ------------------------------------
# TOP PRODUCTS
# ------------------------------------
st.subheader("🏆 Top 10 Products")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    text_auto=".2s",
    color="Sales"
)

st.plotly_chart(fig3, use_container_width=True)

# ------------------------------------
# TOP STATES
# ------------------------------------
st.subheader("🌍 Top 10 States")

top_states = (
    filtered_df.groupby("State")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig4 = px.bar(
    top_states,
    x="State",
    y="Sales",
    color="Sales",
    text_auto=".2s"
)

st.plotly_chart(fig4, use_container_width=True)

# ------------------------------------
# SALES BY SEGMENT
# ------------------------------------
st.subheader("👥 Sales by Segment")

segment = (
    filtered_df.groupby("Segment")["Sales"]
    .sum()
    .reset_index()
)

fig5 = px.bar(
    segment,
    x="Segment",
    y="Sales",
    color="Segment",
    text_auto=".2s"
)

st.plotly_chart(fig5, use_container_width=True)

# ------------------------------------
# AI INSIGHTS
# ------------------------------------
st.subheader("🤖 AI Business Insights")

best_category = filtered_df.groupby("Category")["Sales"].sum().idxmax()
best_state = filtered_df.groupby("State")["Sales"].sum().idxmax()
best_product = filtered_df.groupby("Product Name")["Sales"].sum().idxmax()

st.success(f"🏆 Best Category : {best_category}")
st.info(f"🌍 Best State : {best_state}")
st.success(f"📦 Best Product : {best_product}")

st.divider()

# ------------------------------------
# DOWNLOAD REPORT
# ------------------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download CSV Report",
    data=csv,
    file_name="RetailIQ_Report.csv",
    mime="text/csv"
)

# ------------------------------------
# DATA TABLE
# ------------------------------------
st.subheader("📋 Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

st.success("✅ Dashboard Loaded Successfully")