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

st.set_page_config(page_title="Auto Prices demo", layout="wide")

st.title("Streamlit Auto Dashboard from csv")
st.markdown("testing out python **streamlit** interactive app.")
# add markdown with URL link
st.markdown("based on: [kd nuggets - how to combine streamlit, pandas, plotly](https://www.kdnuggets.com/how-to-combine-streamlit-pandas-and-plotly-for-interactive-data-apps.html)")
st.markdown("using: python streamlit, pandas, numpy, plotly")
# create markdown bullet list using st.markdown
st.markdown("""
            * efficient
            * interactive
            * deploy to streamlit community
            """)

#st.write("This is also a **markdown** paragraph")

# import csv file auto_cleaned.csv from data folder
df_auto = pd.read_csv("data/auto_cleaned.csv")
df = df_auto
# select columns to keep
df_autoc = df_auto[["make", "fuel-type", "num-of-doors", 
                "body-style", "horsepower", 
                "city-L/100km", "highway-L/100km", "price"]]


# sidebar filters
st.sidebar.header("Filters")
make = st.sidebar.multiselect("Select Make", df["make"].unique(), default=df["make"].unique())
fuel = st.sidebar.multiselect("Select Fuel Type", df["fuel-type"].unique(), default=df["fuel-type"].unique())
# numeric range filter for horsepower
hp_min = st.sidebar.number_input("Min Horsepower", min_value=df["horsepower"].min(), max_value=df["horsepower"].max(), value=df["horsepower"].min())
hp_max = st.sidebar.number_input("Max Horsepower", min_value=df["horsepower"].min(), max_value=df["horsepower"].max(), value=df["horsepower"].max())
# numeric range filter for city-L/100km
city_min = st.sidebar.number_input("Min City L/100km", min_value=df["city-L/100km"].min(), max_value=df["city-L/100km"].max(), value=df["city-L/100km"].min())
city_max = st.sidebar.number_input("Max City L/100km", min_value=df["city-L/100km"].min(), max_value=df["city-L/100km"].max(), value=df["city-L/100km"].max())
# numeric range filter for highway-L/100km
highway_min = st.sidebar.number_input("Min Highway L/100km", min_value=df["highway-L/100km"].min(), max_value=df["highway-L/100km"].max(), value=df["highway-L/100km"].min())
highway_max = st.sidebar.number_input("Max Highway L/100km", min_value=df["highway-L/100km"].min(), max_value=df["highway-L/100km"].max(), value=df["highway-L/100km"].max())

# filter data - based on filters above in sidebar
filtered_df = df[(df["make"].isin(make)) & (df["fuel-type"].isin(fuel)) & 
                (df["horsepower"] >= hp_min) & (df["horsepower"] <= hp_max) & 
                (df["city-L/100km"] >= city_min) & (df["city-L/100km"] <= city_max) & 
                (df["highway-L/100km"] >= highway_min) & (df["highway-L/100km"] <= highway_max)]
#filtered_df = df[(df["Region"].isin(region)) & (df["Product"].isin(product))]

# display metrics
col1, col2, col3, col4, col5 = st.columns(5)
# price metrics in dollar format
col1.metric("Min Price", f"${filtered_df['price'].min():,.0f}")
col3.metric("Max Price", f"${filtered_df['price'].max():,.0f}")
col2.metric("Med. Price", f"${filtered_df['price'].median():,.0f}")
col4.metric("Avg. Fuel Eff.", f"{filtered_df['city-L/100km'].mean():,.0f}")
col5.metric("# of options", len(filtered_df))

# charts - plotly
col1, col2, col3 = st.columns(3)

# histogram plot with plotly showing price distribution
with col1:
    fig_hist = px.histogram(filtered_df, x="price", title="Price Distribution")
    st.plotly_chart(fig_hist, use_container_width=True)

# box plot with plotly showing price distribution by make
with col2:
    fig_box = px.box(filtered_df, x="make", y="price", title="Price Distribution by Make")
    st.plotly_chart(fig_box, use_container_width=True)

# scatter plot with plotly showing price by city-L/100km
# color by make
with col3:
    fig_scatter = px.scatter(filtered_df, x="city-L/100km", y="price", title="Price by Fuel Efficiency", color="make")
    st.plotly_chart(fig_scatter, use_container_width=True)

# display filtered data - after filters change
st.subheader("Filtered Data")
st.write("Filtered data based on filters above in sidebar")
# remove index column
filter_df = filtered_df.reset_index(drop=True)
st.dataframe(filter_df)