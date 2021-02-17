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