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
st.subheader("Explore Road Conditions and Transportation")

road_type = st.selectbox(
    "Select a road type:",
    ["Main Roads", "Secondary Roads", "Agricultural Roads"]
)
road_condition = st.selectbox(
    "Select a road condition:",
    ["Good", "Acceptable", "Bad"]
)
road_columns = {
    "Main Roads": {
        "Good": "State of the main roads - good",
        "Acceptable": "State of the main roads - acceptable",
        "Bad": "State of the main roads - bad"
    },
    "Secondary Roads": {
        "Good": "State of the secondary roads - good",
        "Acceptable": "State of the secondary roads - acceptable",
        "Bad": "State of the secondary roads - bad"
    },
    "Agricultural Roads": {
        "Good": "State of agricultural roads - good",
        "Acceptable": "State of agricultural roads - acceptable",
        "Bad": "State of agricultural roads - bad"
    }
}

selected_column = road_columns[road_type][road_condition]

filtered_df = df[df[selected_column] == 1]
road_data = pd.DataFrame({
    "Road Type": ["Main Roads", "Secondary Roads", "Agricultural Roads"],
    "Good": [
        df["State of the main roads - good"].sum(),
        df["State of the secondary roads - good"].sum(),
        df["State of agricultural roads - good"].sum()
    ],
    "Acceptable": [
        df["State of the main roads - acceptable"].sum(),
        df["State of the secondary roads - acceptable"].sum(),
        df["State of agricultural roads - acceptable"].sum()
    ],
    "Bad": [
        df["State of the main roads - bad"].sum(),
        df["State of the secondary roads - bad"].sum(),
        df["State of agricultural roads - bad"].sum()
    ]
})

heatmap_data = road_data.set_index("Road Type")

fig1 = px.imshow(
    heatmap_data,
    text_auto=True,
    labels=dict(x="Road Condition", y="Road Type", color="Number of Towns"),
    title="Road Conditions Across Lebanese Towns"
)

st.plotly_chart(fig1, use_container_width=True)
filtered_df = filtered_df.copy()

filtered_df["Transport Combination"] = filtered_df.apply(
    lambda row: " + ".join([
        mode for mode, column in {
            "Taxi": "The main means of public transport - taxis",
            "Van": "The main means of public transport - vans",
            "Bus": "The main means of public transport - buses"
        }.items()
        if row[column] == 1
    ]) or "None Reported",
    axis=1
)

transport_combinations = (
    filtered_df["Transport Combination"]
    .value_counts()
    .reset_index()
)

transport_combinations.columns = ["Transport Combination", "Number of Towns"]

fig2 = px.scatter(
    transport_combinations,
    x="Number of Towns",
    y="Transport Combination",
    size="Number of Towns",
    title=f"Transportation Combinations in Towns with {road_condition} {road_type}",
    labels={"Number of Towns": "Number of Towns"}
)

st.plotly_chart(fig2, use_container_width=True)
