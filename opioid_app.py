import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np

from sqlalchemy import create_engine
# getting data from git

specialty = pd.read_csv('specialty_data.csv')
city = pd.read_csv('city_data.csv')
opioid_zip_codes = pd.read_csv('opioid_zip_codes.csv')

# start of the application
st.header('question 1')
st.subheader('Which Tennessee counties had a disproportionately high number of opioid prescriptions?')

st.header('question 2')
st.subheader('Who are the top opioid prescribers for the state of Tennessee?')

fig = px.bar(specialty, x='total_claim', y='specialty_description',
title='Most prescribed Methadone by Specialty')
fig

fig1 = px.bar(city, x='total_claim', y='nppes_provider_city',
title='Most prescribed Methadone by City')
fig1

st.dataframe(opioid_zip_codes)


st.header('question 3')
st.subheader('What did the trend in overdose deaths due to opioids look like in Tennessee from 2015 to 2018?')

st.header('question 4')
st.subheader('Is there an association between rates of opioid prescriptions and overdose deaths by county?')

st.header('question 5')
st.subheader('Is there any association between a particular type of opioid and number of overdose deaths?')