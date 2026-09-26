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
st.markdown("""
### What does the data show?

The data reveals two key patterns in how main-road conditions relate to public transportation across Lebanese towns:

**Insight 1: Vans become more common as main-road conditions worsen.** Van availability rises from **27.9% of towns with good main roads** to **37.1% with bad main roads**, while taxi availability decreases slightly from **88.5% to 82.7%**.

**Insight 2: Poorer main-road conditions are associated with a shift away from taxi-only transportation toward Taxi + Van combinations.** Taxi-only falls from **64.8% of towns with good main roads** to **57.7% with bad main roads**, while Taxi + Van rises from **12.3% to 17.3%**.
""")
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
# VISUALIZATION 1: Transportation availability by road condition

transport_columns = {
    "Taxi": "The main means of public transport - taxis",
    "Van": "The main means of public transport - vans",
    "Bus": "The main means of public transport - buses"
}

visual1_data = []

for condition in ["Good", "Acceptable", "Bad"]:
    condition_column = road_columns[road_type][condition]
    condition_df = df[df[condition_column] == 1]
    
    for mode, column in transport_columns.items():
        percentage = condition_df[column].mean() * 100
        
        visual1_data.append({
            "Road Condition": condition,
            "Transportation Mode": mode,
            "Availability (%)": percentage
        })

visual1_df = pd.DataFrame(visual1_data)

fig1 = px.bar(
    visual1_df,
    x="Road Condition",
    y="Availability (%)",
    color="Transportation Mode",
    barmode="group",
    text_auto=".1f",
    title=f"Public Transportation Availability by {road_type} Condition",
    category_orders={
        "Road Condition": ["Good", "Acceptable", "Bad"],
        "Transportation Mode": ["Taxi", "Van", "Bus"]
    }
)

fig1.update_layout(
    yaxis_title="Percentage of Towns (%)",
    xaxis_title="Road Condition"
)

st.plotly_chart(fig1, use_container_width=True)


# VISUALIZATION 2: Transportation combinations across road conditions

combination_data = []

for condition in ["Good", "Acceptable", "Bad"]:
    condition_column = road_columns[road_type][condition]
    condition_df = df[df[condition_column] == 1].copy()

    condition_df["Transport Combination"] = condition_df.apply(
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

    counts = condition_df["Transport Combination"].value_counts()
    total = len(condition_df)

    for combination, count in counts.items():
        combination_data.append({
            "Road Condition": condition,
            "Transport Combination": combination,
            "Percentage of Towns": (count / total) * 100
        })

combination_df = pd.DataFrame(combination_data)

fig2 = px.bar(
    combination_df,
    x="Transport Combination",
    y="Percentage of Towns",
    color="Road Condition",
    barmode="group",
    text_auto=".1f",
    title=f"Transportation Combinations by {road_type} Condition",
    category_orders={
        "Road Condition": ["Good", "Acceptable", "Bad"]
    }
)

fig2.update_layout(
    xaxis_title="Transportation Combination",
    yaxis_title="Percentage of Towns (%)"
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
