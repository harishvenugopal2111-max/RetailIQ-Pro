import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="Forecast", page_icon="📈", layout="wide")

st.title("📈 Sales Forecast")

# Load Data
df = pd.read_csv("data/clean_superstore.csv")

# Safe Date Conversion
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df = df.dropna(subset=["Order Date"])

# Monthly Sales
monthly = (
    df.resample("ME", on="Order Date")["Sales"]
      .sum()
      .reset_index()
)

# Model
monthly["Month"] = np.arange(len(monthly))

X = monthly[["Month"]]
y = monthly["Sales"]

model = LinearRegression()
model.fit(X, y)

# Future Prediction
future_months = np.arange(
    len(monthly),
    len(monthly) + 6
).reshape(-1, 1)

predictions = model.predict(future_months)

# Future Dates
last_date = monthly["Order Date"].max()

future_dates = pd.date_range(
    start=last_date + pd.offsets.MonthEnd(1),
    periods=6,
    freq="ME"
)

forecast = pd.DataFrame({
    "Date": future_dates,
    "Predicted Sales": predictions
})

# KPI
c1, c2 = st.columns(2)

c1.metric(
    "Current Avg Sales",
    f"${monthly['Sales'].mean():,.2f}"
)

c2.metric(
    "Next Month Prediction",
    f"${predictions[0]:,.2f}"
)

st.divider()

# Historical
fig1 = px.line(
    monthly,
    x="Order Date",
    y="Sales",
    title="Historical Monthly Sales",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# Forecast
fig2 = px.line(
    forecast,
    x="Date",
    y="Predicted Sales",
    title="Next 6 Months Forecast",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Forecast Table")
st.dataframe(forecast, use_container_width=True)

if predictions[-1] > predictions[0]:
    st.success("📈 Forecast shows an increasing sales trend.")
else:
    st.warning("📉 Forecast shows a decreasing sales trend.")