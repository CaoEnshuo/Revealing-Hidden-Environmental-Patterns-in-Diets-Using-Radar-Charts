import pandas as pd
import plotly.express as px

# Step 1: Load the dataset
df = pd.read_csv("Results_21Mar2022.csv")

# Step 2: Select fields for the radar chart
radar_vars = [
    "mean_ghgs",         # Greenhouse Gas Emissions
    "mean_land",         # Land Use
    "mean_watscar",      # Water Scarcity
    "mean_eut",          # Eutrophication
    "mean_ghgs_ch4",     # Methane
    "mean_ghgs_n2o",     # Nitrous Oxide
    "mean_bio",          # Biodiversity Impact
    "mean_watuse",       # Agricultural Water Use
    "mean_acid"          # Acidification
]

# Step 3: Aggregate and normalize the data
grouped_df = df.groupby("diet_group").mean(numeric_only=True)
radar_data = grouped_df[radar_vars]
normalized_data = (radar_data - radar_data.min()) / (radar_data.max() - radar_data.min())

# Step 4: Transform the data into long format
plot_data = normalized_data.copy()
plot_data["Diet Group"] = plot_data.index
plot_data_long = plot_data.melt(id_vars="Diet Group", var_name="Indicator", value_name="Value")

# Step 5: Replace variable labels with full names
label_dict = {
    "mean_ghgs": "Greenhouse Gas Emissions",
    "mean_land": "Land Use",
    "mean_watscar": "Water Scarcity",
    "mean_eut": "Eutrophication Potential",
    "mean_ghgs_ch4": "Methane Emissions",
    "mean_ghgs_n2o": "Nitrous Oxide Emissions",
    "mean_bio": "Biodiversity Impact",
    "mean_watuse": "Agricultural Water Use",
    "mean_acid": "Acidification Potential"
}
plot_data_long["Indicator"] = plot_data_long["Indicator"].map(label_dict)

# Step 6: Create the radar chart
fig = px.line_polar(
    plot_data_long,
    r="Value",
    theta="Indicator",
    color="Diet Group",
    line_close=True,
    title="Environmental Impact by Diet Group",
    template="plotly_dark"
)

# Step 7: Adjust visual styles and layout
fig.update_traces(fill='toself')
fig.update_layout(
    title=dict(
        text="Environmental Impact by Diet Group",
        x=0.5,
        xanchor='center'
    ),
    legend=dict(
        font=dict(size=18),
        x=0.8,
        y=0.85,
        bgcolor="rgba(0,0,0,0)"
    ),
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 1])
    ),
    margin=dict(l=50, r=50, t=80, b=50)
)

# Step 8: Export the chart as an HTML file
fig.write_html("environmental_impact_radar_v2_tight_biglegend.html")
