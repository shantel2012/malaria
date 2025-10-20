# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------
# PAGE CONFIG
# ---------------------
st.set_page_config(page_title="Malaria Dashboard", layout="wide")

# ---------------------
# CUSTOM STYLING
# ---------------------
st.markdown(
    """
    <style>
        body { background-color: #f8f9fa; color: #333; }
        .block-container { padding-top: 1rem; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------
# HEADER
# ---------------------
st.title("🦟 Malaria Dashboard")
st.caption("Simple data exploration and visualization")

# ---------------------
# FILE UPLOAD
# ---------------------
uploaded_file = st.file_uploader("Upload your malaria data (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📋 Data Preview")
    st.dataframe(df, use_container_width=True)

    # ---------------------
    # BASIC STATS
    # ---------------------
    st.subheader("📊 Key Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Records", len(df))
    with col2:
        if "cases" in df.columns:
            st.metric("Total Cases", int(df["cases"].sum()))
        else:
            st.metric("Total Cases", "N/A")
    with col3:
        if "region" in df.columns:
            st.metric("Regions", df["region"].nunique())
        else:
            st.metric("Regions", "N/A")

    # ---------------------
    # CHARTS
    # ---------------------
    st.subheader("📈 Charts")

    if "region" in df.columns and "cases" in df.columns:
        fig = px.bar(
            df.groupby("region", as_index=False)["cases"].sum(),
            x="region", y="cases",
            color="region",
            title="Malaria Cases by Region",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

    if "month" in df.columns and "cases" in df.columns:
        fig2 = px.line(
            df, x="month", y="cases",
            color="region" if "region" in df.columns else None,
            title="Monthly Malaria Trends",
            template="plotly_white"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ---------------------
    # MAP
    # ---------------------
    if {"latitude", "longitude"}.issubset(df.columns):
        st.subheader("🗺️ Case Map")
        st.map(df[["latitude", "longitude"]])

    # ---------------------
    # RAW DATA
    # ---------------------
    st.subheader("📄 Full Dataset")
    st.dataframe(df, use_container_width=True)
else:
    st.info("👆 Upload a CSV file to begin.")
