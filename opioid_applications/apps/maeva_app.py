import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np
import plotly.graph_objects as go

# Added By Maeva
import json


url1 ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/maeva/data/opioid_deaths_yearly_trend_tn.csv'
url2 ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/maeva/data/opioid_prescriptions_tn.csv'

opioid_prescriptions_tn = pd.read_csv(url2)
opioid_deaths_yearly_trend_tn = pd.read_csv(url1)


from sqlalchemy import create_engine


# start of the application visuals
# question 1
st.header('question 1')
st.subheader('Which Tennessee counties had a disproportionately high number of opioid prescriptions?')

## ---- 1st Map ----
"""
#### State-wide Distribution of Unweighted Opioid Prescriptions Per County
"""

with open('geojson-counties-fips.json') as f:
    counties_geo = json.load(f)

fig = go.Figure(go.Choroplethmapbox(
    geojson=counties_geo, 
    locations=opioid_prescriptions_tn['fipscounty'], 
    z=opioid_prescriptions_tn['opioid_prescriptions'],
    colorscale="portland", 
    zmin=opioid_prescriptions_tn['opioid_prescriptions'].min(), 
    zmax=opioid_prescriptions_tn['opioid_prescriptions'].max(),
    marker_opacity=0.6, 
    marker_line_width=0,
    text=opioid_prescriptions_tn['county'],
    name='Unweighted Opioid Prescription',
    hovertemplate =
    '<b>%{text}</b>'+
    '<br>%{z:.1f}',
))
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=6, 
    mapbox_center = {"lat": 35.9631344, "lon": -85.8566687}
)
fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    title="State-wide Distribution of Unweighted Opioid Prescriptions Per County"
)
fig

## ---- /End 1st Map ----

## ---- 1st Graph ----
# Define the base figure
fig = go.Figure()

# Add trace for proportion of opioid prescriptions per prescriber
fig.add_trace(go.Bar(
    x=opioid_prescriptions_tn['county'],
    y=opioid_prescriptions_tn['opioid_prescription_per_prescriber'],
    name='Prescriptions Per Prescribers Ratio',
    orientation='v',
    hovertemplate =
    '<b>%{x}</b>'+
    '<br>%{y:.1f}',
    marker=dict(
        color='rgba(50, 50, 200, 1.0)',
        #line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    )
))
# Add figure styles using update_layout
fig.update_layout(
    title="Opioid Prescriptions Per Prescribers Per County Ratio",
    hoverlabel_align='left',
    #barmode='stack', 
    barmode='group',
    width=1700,
    xaxis={
        'title': 'TN County',
        'tickangle': -45,
        'categoryorder': 'array',
        'categoryarray': [x for _, x in sorted(zip(opioid_prescriptions_tn['opioid_prescription_per_prescriber'], opioid_prescriptions_tn['county']), reverse=True)]
    },
    yaxis={
        'title': "Opioid Prescriptions Per Prescribers"
    }
)
# Show figure
fig
## ---- /End 1st Graph ----
## ---- 2nd Graph ----
df = opioid_prescriptions_tn.loc[:, ['county','opioid_prescription_per_prescriber']].copy()

fig = px.box(
    df,
    x='opioid_prescription_per_prescriber',
    hover_name='county',
    labels={
        "opioid_prescription_per_prescriber": "Opioid Prescriptions Per Prescriber",
     },
    title="State-wide Distribution of Opioid Prescriptions Per County Weighted By Prescribers Per County"
)

fig
## ---- /End 2nd Graph ----

## ---- 2nd Map ----
"""
#### State-wide Distribution of Opioid Prescriptions Per County Weighted By Prescribers Per County
"""

fig = go.Figure(go.Choroplethmapbox(
    geojson=counties_geo, 
    locations=opioid_prescriptions_tn['fipscounty'], 
    z=opioid_prescriptions_tn['opioid_prescription_per_prescriber'],
    colorscale="portland", 
    zmin=opioid_prescriptions_tn['opioid_prescription_per_prescriber'].min(), 
    zmax=opioid_prescriptions_tn['opioid_prescription_per_prescriber'].max(),
    marker_opacity=0.6, 
    marker_line_width=0,
    text=opioid_prescriptions_tn['county'],
    name='Opioid Prescription/Prescribers Ratio',
    hovertemplate =
    '<b>%{text}</b>'+
    '<br>%{z:.1f}',
))
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=6, 
    mapbox_center = {"lat": 35.9631344, "lon": -85.8566687}
)
fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    title="State-wide Distribution of Opioid Prescriptions Per County Weighted By Prescribers Per County"
)
fig
## ---- /End 2nd Map ----

"""
 **Conclusion:** When weighting by *Prescribers By County*, we see that the following counties have way too much opioid prescriptions rate relative to the median opioid prescriptions per prescribers across all counties (1.84):
- Trousdale: 3.4 opioid prescriptions per county's available prescribers
- Chester: 3.41 opioid prescriptions per county's available prescribers
- Benton: 3.63 opioid prescriptions per county's available prescribers
- Van Buren: 3.67 opioid prescriptions per county's available prescribers
- Morgan: 3.73 opioid prescriptions per county's available prescribers
- Clay: 4.92 opioid prescriptions per county's available prescribers
"""

## ---- 3rd Graph ----
opioid_prescriptions_tn['opioid_prescription_population_ratio'] = opioid_prescriptions_tn['opioid_prescriptions'] / opioid_prescriptions_tn['population']
opioid_prescriptions_tn['opioid_prescription_population_ratio_1k'] = opioid_prescriptions_tn['opioid_prescriptions'] / opioid_prescriptions_tn['population'] * 1000

df = opioid_prescriptions_tn.loc[:, ['county','opioid_prescription_population_ratio_1k']].copy()

fig = px.box(
    df,
    x='opioid_prescription_population_ratio_1k',
    hover_name='county',
    labels={
        "opioid_prescription_per_prescriber": "Opioid Prescriptions Per 10k Population",
     },
    title="State-wide Distribution of Opioid Prescriptions Per County Weighted By Population Per County (in 1k)"
)

fig
## ---- /End 3rd Graph ----


"""
**Conclusion:** When weighting by *Population By County*, we see that the following counties have way too much opioid prescriptions rate relative to the median opioid prescriptions per population across all counties (3.51):
- Putnam: 7.66 opioid prescriptions per county's 1k population
- Clay: 7.68 opioid prescriptions per county's 1k population
- Coffee: 8.23 opioid prescriptions per county's 1k population
- Putnam: 8.94 opioid prescriptions per county's 1k population
- Madison: 9.41 opioid prescriptions per county's 1k population
- Washington: 11.07 opioid prescriptions per county's 1k population
"""


## --- \End of Question 1 ----