import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Road Conditions & Public Transportation in Lebanon",
    layout="wide"
)

df = pd.read_csv("dataset.csv")

st.title("Road Conditions & Public Transportation in Lebanon")

st.write(
    "This interactive dashboard explores how road conditions in Lebanese towns "
    "relate to the availability of different public transportation modes."
)
