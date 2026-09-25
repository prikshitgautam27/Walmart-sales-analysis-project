"""
Walmart Sales - Interactive Dashboard
---------------------------------------
Run with:
    streamlit run dashboard/app.py

Requires: streamlit, pandas, plotly (see requirements.txt)
"""

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Walmart Sales Dashboard", layout="wide")

DATA_PATH = "data/walmart_clean_data.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%y", errors="coerce")
    return df


df = load_data()

st.title("Walmart Sales Performance Dashboard")
st.caption("Interactive view of branch, category and payment method performance")

# ---- Sidebar filters ----
st.sidebar.header("Filters")
cities = st.sidebar.multiselect("City", sorted(df["city"].unique()), default=None)
categories = st.sidebar.multiselect("Category", sorted(df["category"].unique()), default=None)

filtered = df.copy()
if cities:
    filtered = filtered[filtered["city"].isin(cities)]
if categories:
    filtered = filtered[filtered["category"].isin(categories)]

# ---- KPI row ----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${filtered['total'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered['profit'].sum():,.0f}")
col3.metric("Transactions", f"{len(filtered):,}")
col4.metric("Avg Rating", f"{filtered['rating'].mean():.2f}")

st.divider()

# ---- Charts ----
c1, c2 = st.columns(2)

with c1:
    rev_by_city = (
        filtered.groupby("city")["total"].sum().sort_values(ascending=False).head(10).reset_index()
    )
    fig = px.bar(rev_by_city, x="city", y="total", title="Top 10 Cities by Revenue")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    profit_by_cat = filtered.groupby("category")["profit"].sum().sort_values(ascending=False).reset_index()
    fig = px.bar(profit_by_cat, x="category", y="profit", title="Total Profit by Category")
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    pay_counts = filtered["payment_method"].value_counts().reset_index()
    pay_counts.columns = ["payment_method", "count"]
    fig = px.pie(pay_counts, names="payment_method", values="count", title="Payment Method Share")
    st.plotly_chart(fig, use_container_width=True)

with c4:
    filtered["hour"] = pd.to_datetime(filtered["time"], format="%H:%M:%S", errors="coerce").dt.hour
    filtered["shift"] = filtered["hour"].apply(
        lambda h: "Morning" if h < 12 else ("Afternoon" if h < 18 else "Evening")
    )
    shift_counts = filtered["shift"].value_counts().reset_index()
    shift_counts.columns = ["shift", "count"]
    fig = px.bar(shift_counts, x="shift", y="count", title="Transactions by Shift")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---- Profit per unit table (extended insight) ----
st.subheader("Profit per Unit Sold by Category")
st.caption("A category with high total profit but low profit-per-unit is a volume play, not a margin play.")
ppu = filtered.groupby("category").agg(
    total_profit=("profit", "sum"),
    total_qty=("quantity", "sum"),
)
ppu["profit_per_unit"] = (ppu["total_profit"] / ppu["total_qty"]).round(2)
st.dataframe(ppu.sort_values("profit_per_unit", ascending=False), use_container_width=True)
