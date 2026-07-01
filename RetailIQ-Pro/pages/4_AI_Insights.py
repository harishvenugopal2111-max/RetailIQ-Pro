import streamlit as st
import pandas as pd
from utils.loader import load_data

st.set_page_config(
    page_title="AI Insights",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Business Insights")

df = load_data()

# ---------------- KPI ----------------
sales = df["Sales"].sum()
profit = df["Profit"].sum()
orders = len(df)

c1, c2, c3 = st.columns(3)

c1.metric("💰 Total Sales", f"${sales:,.2f}")
c2.metric("📈 Total Profit", f"${profit:,.2f}")
c3.metric("🛒 Orders", orders)

st.divider()

# ---------------- BEST CATEGORY ----------------
best_category = (
    df.groupby("Category")["Sales"]
    .sum()
    .idxmax()
)

best_category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .max()
)

st.success(
    f"🏆 Best Category : {best_category}\n\nSales : ${best_category_sales:,.2f}"
)

# ---------------- BEST STATE ----------------
best_state = (
    df.groupby("State")["Sales"]
    .sum()
    .idxmax()
)

best_state_sales = (
    df.groupby("State")["Sales"]
    .sum()
    .max()
)

st.info(
    f"🌍 Best State : {best_state}\n\nSales : ${best_state_sales:,.2f}"
)

# ---------------- TOP PRODUCT ----------------
best_product = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .idxmax()
)

best_product_sales = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .max()
)

st.success(
    f"📦 Best Product : {best_product}\n\nSales : ${best_product_sales:,.2f}"
)

# ---------------- LOSS PRODUCTS ----------------
st.subheader("📉 Top Loss Making Products")

loss = (
    df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values()
    .head(10)
)

st.dataframe(loss)

# ---------------- TOP PROFIT PRODUCTS ----------------
st.subheader("💰 Top Profit Products")

profit_products = (
    df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(profit_products)

# ---------------- RECOMMENDATIONS ----------------
st.subheader("🤖 AI Recommendations")

recommendations = []

if df.groupby("Category")["Sales"].sum().idxmax() == "Technology":
    recommendations.append(
        "Increase Technology inventory because it generates the highest sales."
    )

if df["Discount"].mean() > 0.20:
    recommendations.append(
        "Average discount is high. Reduce discounts to improve profit."
    )

if df["Profit"].sum() > 0:
    recommendations.append(
        "Overall business is profitable."
    )
else:
    recommendations.append(
        "Business is running at a loss."
    )

for i, rec in enumerate(recommendations, start=1):
    st.write(f"{i}. {rec}")

# ---------------- SUMMARY ----------------
st.divider()

st.success("✅ AI Insights Generated Successfully")
