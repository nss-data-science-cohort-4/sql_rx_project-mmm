import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np

q2_url ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/mg_opioid_branch/opioid_zip_codes.csv'

q2_df= pd.read_csv(q2_url)

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