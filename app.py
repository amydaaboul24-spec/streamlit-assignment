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
# VISUALIZATION 1: Selected road condition
selected_road_data = pd.DataFrame({
    "Road Condition": ["Good", "Acceptable", "Bad"],
    "Number of Towns": [
        df[road_columns[road_type]["Good"]].sum(),
        df[road_columns[road_type]["Acceptable"]].sum(),
        df[road_columns[road_type]["Bad"]].sum()
    ]
})

fig1 = px.bar(
    selected_road_data,
    x="Road Condition",
    y="Number of Towns",
    title=f"Road Conditions for {road_type}",
    text="Number of Towns"
)

fig1.update_traces(
    marker_line_width=[
        3 if condition == road_condition else 0
        for condition in selected_road_data["Road Condition"]
    ]
)

st.plotly_chart(fig1, use_container_width=True)


# VISUALIZATION 2: Transportation combinations
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

transport_combinations.columns = [
    "Transport Combination",
    "Number of Towns"
]

fig2 = px.scatter(
    transport_combinations,
    x="Number of Towns",
    y="Transport Combination",
    size="Number of Towns",
    title=f"Transportation Combinations in Towns with {road_condition} {road_type}",
    labels={"Number of Towns": "Number of Towns"}
)

st.plotly_chart(fig2, use_container_width=True)
# OPTIONAL TOWN EXPLORER
st.subheader("Explore Matching Towns")

st.write(
    f"View the towns with **{road_condition.lower()} {road_type.lower()}** "
    "and filter them by transportation mode."
)

transport_filter = st.selectbox(
    "Filter towns by transportation:",
    ["All", "Taxi", "Van", "Bus"]
)

town_results = filtered_df.copy()

transport_columns = {
    "Taxi": "The main means of public transport - taxis",
    "Van": "The main means of public transport - vans",
    "Bus": "The main means of public transport - buses"
}

if transport_filter != "All":
    town_results = town_results[
        town_results[transport_columns[transport_filter]] == 1
    ]

town_column = "Town"

if town_column in town_results.columns:
    towns = (
        town_results[[town_column]]
        .dropna()
        .drop_duplicates()
        .sort_values(town_column)
    )

    st.write(f"**{len(towns)} matching towns**")
    st.dataframe(towns, use_container_width=True, hide_index=True)
else:
    st.warning("Town-name column could not be found in the dataset.")
