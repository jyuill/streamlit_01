import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# test
#a = 1+2
#b = a+3
#st.write(b) # prints in streamlit window
#print(b) # prints in terminal, if 

st.set_page_config(page_title="Page Tab Title", layout="wide")

st.title("Streamlit Dashboard")
st.markdown("testing out python **streamlit** interactive app. from example on kdnuggets.com")

#st.write("This is a **markdown** paragraph")

# generate sample data
np.random.seed(40)
df = pd.DataFrame({
    "Date": pd.date_range("2024-01-01", periods=100), 
    "Sales": np.random.randint(500, 2000, size=100),
    "Region": np.random.choice(["East", "West", "North", "South"], size=100),
    "Product": np.random.choice(["Sinto", "Wrecher", "Plusmo", "Depty"], size=100)
    }
)

# sidebar filters
st.sidebar.header("Filters")
region = st.sidebar.multiselect("Select Region", df["Region"].unique(), default=df["Region"].unique())
product = st.sidebar.multiselect("Select Product", df["Product"].unique(), default=df["Product"].unique())

# filter data
filtered_df = df[(df["Region"].isin(region)) & (df["Product"].isin(product))]

# display metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"{filtered_df['Sales'].sum():,.0f}")
col2.metric("Average Sales", f"{filtered_df['Sales'].mean():,.0f}")
col3.metric("Records", len(filtered_df))

# display filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_df)