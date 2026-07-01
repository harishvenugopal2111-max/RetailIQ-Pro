import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="RetailIQ Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.main{
    background:#0B1120;
}
.block-container{
    padding-top:1rem;
}
div[data-testid="metric-container"]{
    background:#111827;
    border:1px solid #1E40AF;
    border-radius:15px;
    padding:18px;
    box-shadow:0 4px 15px rgba(0,0,0,.25);
}
div[data-testid="metric-container"]:hover{
    border:1px solid #3B82F6;
}
h1,h2,h3{
    color:white;
}
section[data-testid="stSidebar"]{
    background:#111827;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Load ----------------
@st.cache_data
def load_data():
    return pd.read_csv("data/clean_superstore.csv")

df = load_data()

# ---------------- Sidebar ----------------
st.sidebar.title("📊 RetailIQ Pro")
st.sidebar.write("AI Business Dashboard")

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

filtered = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

# ---------------- Header ----------------
st.markdown("""
# 👋 Welcome Harish

### AI Powered Business Intelligence Dashboard
""")

st.divider()

# ---------------- KPI ----------------
sales = filtered["Sales"].sum()
profit = filtered["Profit"].sum()
orders = len(filtered)
quantity = filtered["Quantity"].sum()

c1,c2,c3,c4 = st.columns(4)

c1.metric("💰 Total Sales",f"${sales:,.2f}")
c2.metric("📈 Profit",f"${profit:,.2f}")
c3.metric("🛒 Orders",orders)
c4.metric("📦 Quantity",int(quantity))

st.divider()
# ---------------- Charts ----------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("📊 Sales by Category")

    category_sales = (
        filtered.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        text_auto=".2s"
    )

    fig.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    st.subheader("🌍 Profit by Region")

    region_profit = (
        filtered.groupby("Region")["Profit"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        region_profit,
        names="Region",
        values="Profit",
        hole=0.55
    )

    fig2.update_layout(
        paper_bgcolor="#111827",
        font_color="white"
    )

    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------------- Top Products ----------------

left, right = st.columns(2)

with left:

    st.subheader("🏆 Top 10 Products")

    top_products = (
        filtered.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    st.dataframe(
        top_products,
        use_container_width=True
    )

with right:

    st.subheader("🏙 Top 10 States")

    top_states = (
        filtered.groupby("State")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    st.dataframe(
        top_states,
        use_container_width=True
    )

st.divider()

# ---------------- AI Insights ----------------

st.subheader("🤖 AI Business Insights")

best_category = (
    filtered.groupby("Category")["Sales"]
    .sum()
    .idxmax()
)

best_state = (
    filtered.groupby("State")["Sales"]
    .sum()
    .idxmax()
)

best_product = (
    filtered.groupby("Product Name")["Sales"]
    .sum()
    .idxmax()
)

c1, c2, c3 = st.columns(3)

with c1:
    st.success(f"🏆 Best Category\n\n{best_category}")

with c2:
    st.info(f"🌍 Best State\n\n{best_state}")

with c3:
    st.success(f"📦 Best Product\n\n{best_product}")

st.divider()

# ---------------- Dataset ----------------

st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered.head(100),
    use_container_width=True
)

csv = filtered.to_csv(index=False)

st.download_button(
    "📥 Download Report",
    csv,
    "RetailIQ_Report.csv",
    "text/csv",
    use_container_width=True
)

st.markdown("---")

st.markdown(
"""
<center>

Made with ❤️ by <b>Harish Venugopal</b>

RetailIQ Pro • AI Powered Business Intelligence Dashboard

</center>
""",
unsafe_allow_html=True
)