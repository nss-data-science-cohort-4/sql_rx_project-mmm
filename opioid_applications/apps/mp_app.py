import streamlit as st
import pandas as pd
import plotly.express as px
import plotly
from ipywidgets import interact, interactive, fixed, interact_manual


#import numpy as np - #Matthew - this is not used for the presentation visuals.
#import matplotlib.pyplot as plt - #Matthew - this is not used for the presentation visuals.
# import plotly.graph_objects as go - #Matthew - this is not used for the presentation visuals.
#from ipywidgets import GridspecLayout - #Matthew - this is not used for the presentation visuals.
#import ipywidgets as widgets - #Matthew - this is not used for the presentation visuals.


url_mp_q4 ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/parker_branch/df4.csv'
url_mp_q5 ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/parker_branch/opioid_df_5.csv'

df4 = pd.read_csv(url_mp_q4)
df_5 =pd.read_csv(url_mp_q5)

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