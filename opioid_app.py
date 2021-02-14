import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np
import plotly.graph_objects as go

from sqlalchemy import create_engine
# getting data from git
url ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/mg_branch/specialty_data.csv'

url1 ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/maeva/data/opioid_deaths_yearly_trend_tn.csv'
url2 ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/maeva/data/opioid_prescriptions_tn.csv'
url3 = 'https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/mg_branch/city_opioid.csv'
#url4

# converting csv 
specialty = pd.read_csv(url)
opioid_zip_codes = pd.read_csv('opioid_zip_codes.csv')
opioid_prescriptions_tn = pd.read_csv(url2)
opioid_deaths_yearly_trend_tn = pd.read_csv(url1)
test = pd.read_csv(url3)

# start of the application visuals
# question 1
st.header('question 1')
st.subheader('Which Tennessee counties had a disproportionately high number of opioid prescriptions?')
st.dataframe(opioid_prescriptions_tn)




# question 1
st.header('question 2')
st.subheader('Who are the top opioid prescribers for the state of Tennessee?')
figed = px.sunburst(test, path=['nppes_provider_city', 'drug_name'], values='total_claim')
figed

# bar plotting perscriptions by specialty

fig_zip = px.scatter_mapbox(opioid_zip_codes, lat="latitude", lon="longitude",color='total_claim', size="total_claim",
                  color_continuous_scale=px.colors.cyclical.Edge, size_max=15, zoom=5,
                  mapbox_style="carto-positron")
fig_zip

# question 3
st.header('question 3')
st.subheader('What did the trend in overdose deaths due to opioids look like in Tennessee from 2015 to 2018?')
# question 4
st.header('question 4')
st.subheader('Is there an association between rates of opioid prescriptions and overdose deaths by county?')
# question 5
st.header('question 5')
st.subheader('Is there any association between a particular type of opioid and number of overdose deaths?')