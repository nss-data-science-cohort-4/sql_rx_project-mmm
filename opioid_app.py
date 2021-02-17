import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
import json


from sqlalchemy import create_engine
# getting data from git
q2_url ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/mg_opioid_branch/opioid_zip_codes.csv'
url1 ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/maeva/data/opioid_deaths_yearly_trend_tn.csv'
url2 ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/maeva/data/opioid_prescriptions_tn.csv'
url_mp_q4 ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/parker_branch/df4.csv'
url_mp_q5 ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/parker_branch/opioid_df_5.csv'


# converting csv 
opioid_prescriptions_tn = pd.read_csv(url2)
opioid_deaths_yearly_trend_tn = pd.read_csv(url1)
df4 = pd.read_csv(url_mp_q4)
df_5 =pd.read_csv(url_mp_q5)
q2_df= pd.read_csv(q2_url)

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

## ---- 3rd Map ----
"""
#### State-wide Distribution of Opioid Prescriptions Per County Weighted By Population Per County (in 1k)
"""
fig = go.Figure(go.Choroplethmapbox(
    geojson=counties_geo, 
    locations=opioid_prescriptions_tn['fipscounty'], 
    z=opioid_prescriptions_tn['opioid_prescription_population_ratio_1k'],
    colorscale="portland", 
    zmin=opioid_prescriptions_tn['opioid_prescription_population_ratio_1k'].min(), 
    zmax=opioid_prescriptions_tn['opioid_prescription_population_ratio_1k'].max(),
    marker_opacity=0.6, 
    marker_line_width=0,
    text=opioid_prescriptions_tn['county'],
    name='Opioid Prescription/Population Ratio (Per 1000)',
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
    title="State-wide Distribution of Opioid Prescriptions Per County Weighted By Population Per County (in 1k)"
)
fig
## ---- /End 3rd Map ----

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



# question 2
st.header('question 2')
st.subheader('Who are the top opioid prescribers for the state of Tennessee?')
#Ui for filtering
# sort variables
sorted_unique_drugs = sorted(q2_df.drug_name.unique())
# create sidebar
selected_drug = st.sidebar.multiselect('Question 2 Drugs filter', sorted_unique_drugs,default="METHADONE HCL")

# function where it filters by selections
df_selected_drugs = q2_df[q2_df.drug_name.isin(selected_drug)]

q2_treefig = px.treemap(q2_df, path=['nppes_provider_zip5', 'drug_name'], values='total_claim',hover_data =['City'])
q2_treefig

st.markdown('The top 3 cities are ** Nashville, Kingsport, and Johnson City**.')

st.subheader('Taking a look at Methadone HCL')
q2_figS = px.treemap(df_selected_drugs, path=['nppes_provider_zip5', 'drug_name'], values='total_claim',hover_data =['City'])
q2_figS

test_fig = px.scatter_mapbox(df_selected_drugs, lat="latitude", lon="longitude",color='total_claim', size="total_claim", 
                  hover_data=['City'],
                  color_continuous_scale=px.colors.cyclical.Edge, size_max=15, zoom=5,
                  mapbox_style="carto-positron")
test_fig

# bar plotting perscriptions by specialty


# question 3
st.header('question 3')
st.subheader('What did the trend in overdose deaths due to opioids look like in Tennessee from 2015 to 2018?')
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=opioid_deaths_yearly_trend_tn['year'], 
        y=opioid_deaths_yearly_trend_tn['opioid_overdose_deaths'],
        mode='lines+markers',
        name='',
        hovertemplate =
        '<b>Year: %{x}</b>'+
        '<br>Deaths: %{y}',
        marker=dict(
            size=15,
            line=dict(
                color='Blue',
                width=2
            )
        )
    )
)
# Add figure styles using update_layout
fig.update_layout(
    title="Overall Trend in Overdose Deaths Due to Opioids In TN (2015 - 2018)",
    xaxis={
        'title': 'Year',
        'tickangle': -45,
        'tickformat': 'd'
    },
    yaxis={
        'title': "Opioid Overdose Deaths"
    }
)
fig



st.header('question 4')
st.subheader('Is there an association between rates of opioid prescriptions and overdose deaths by county?')
mp_q4_fig = px.scatter(df4, x="claims_per_county", y="overdose_deaths", size='population',
           hover_name="county", trendline='ols', trendline_color_override='orange')

mp_q4_fig.update_layout(
    title="Opioid Claims vs. Overdose Deaths in Tennessee (2017)",
    xaxis_title="Total Opioid Claims",
    yaxis_title="Number of Overdose Deaths"
    )
mp_q4_fig


df_5['od_claim_ratio'] = df_5['overdose_deaths'] / df_5['opioid_claims'] * 1000
st.header('question 5')
st.subheader('Is there any association between a particular type of opioid and number of overdose deaths?')


sorted_unique_opioid = sorted(df_5.opioid.unique())
selected_opioid__1 = st.sidebar.multiselect('Question 5 drug filter for chart 1', sorted_unique_opioid,default='codeine')
selected_opioid_2 = st.sidebar.multiselect('Question 5 drug filter for chart 2', sorted_unique_opioid,default='codeine')
selected_opioid_3 = st.sidebar.multiselect('Question 5 drug filter for chart 3', sorted_unique_opioid,default='codeine')
selected_opioid_4 = st.sidebar.multiselect('Question 5 drug filter for chart 4', sorted_unique_opioid,default='codeine')
selected_opioid_5 = st.sidebar.multiselect('Question 5 drug filter for chart 5', sorted_unique_opioid,default='codeine')

df_5_selected_c1 = df_5[df_5.opioid.isin(selected_opioid__1)]
df_5_selected_c2 = df_5[df_5.opioid.isin(selected_opioid_2)]
df_5_selected_c3 = df_5[df_5.opioid.isin(selected_opioid_3)]
df_5_selected_c4 = df_5[df_5.opioid.isin(selected_opioid_4)]
df_5_selected_c5 = df_5[df_5.opioid.isin(selected_opioid_5)]

st.subheader('Total Claims vs ODs, colored by percent of claims by selected opioid')
q5_fig = px.scatter(df_5_selected_c1, x="total_claims", y="overdose_deaths", size='population', color='opioid_percent', color_continuous_scale=['lightgray', 'red', 'darkred'], opacity = 1,
           hover_name="county", size_max=20, trendline='ols', trendline_color_override='orange')
q5_fig

st.subheader('% Claims of Selected Opioid vs. Total ODs')
fig_5_chart2 = px.scatter(df_5_selected_c2, x="opioid_claims", y="overdose_deaths", size='population', 
                     color = 'opioid_percent', color_continuous_scale=['darkgray', 'red'], opacity = 1,
                     hover_name="county", trendline='ols', trendline_color_override='orange')
fig_5_chart2

st.subheader('Total Claims by Selected Opioid vs. OD deaths per claims.')
fig_5_chart3 =px.scatter(df_5_selected_c3, x="opioid_claims", y="od_claim_ratio", size='population', 
                     color = 'opioid_percent', color_continuous_scale=['darkgray', 'red'], opacity = 1,
                     hover_name="county", trendline='ols', trendline_color_override='orange')

fig_5_chart3
st.subheader('% Claims of Selected Opioid vs. ODs per 1,000 opioid prescriptions')
fig_5_chart4 = px.scatter(df_5_selected_c4, x="opioid_percent", y="od_claim_ratio", size='population', 
                     color = 'opioid_percent', color_continuous_scale=['darkgray', 'red'], opacity = 1,
                     hover_name="county", trendline='ols', trendline_color_override='orange', range_x = [0,75])

fig_5_chart4

st.subheader('Percent Claims by selected opioid vs Total Overdose Deaths')
fig_5_chart5 =px.scatter(df_5_selected_c5, x="opioid_percent", y="overdose_deaths", size='population', 
                     color = 'opioid_percent', color_continuous_scale=['darkgray', 'red'], opacity = 1,
                     hover_name="county", trendline='ols', trendline_color_override='orange')
fig_5_chart5


st.markdown("![Alt Text](https://media.giphy.com/media/AkLGHCYGv43uw/giphy.gif)") 