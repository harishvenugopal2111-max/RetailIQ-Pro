import streamlit as st
import plotly.express as px
from models.customer_segmentation import customer_segmentation

st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Customer Segmentation")

df = customer_segmentation()

st.dataframe(df)

fig = px.scatter(
    df,
    x="Sales",
    y="Profit",
    color=df["Cluster"].astype(str),
    size="Quantity",
    title="Customer Segments"
)

st.plotly_chart(fig, use_container_width=True)
