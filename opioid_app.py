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
q2_url ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/mg_branch/opioid_zip_codes.csv'
url1 ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/maeva/data/opioid_deaths_yearly_trend_tn.csv'
url2 ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/maeva/data/opioid_prescriptions_tn.csv'
url_mp_q4 ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/parker_branch/df4.csv'
url_mp_q5 ='https://raw.githubusercontent.com/nss-data-science-cohort-4/sql_rx_project-mmm/parker_branch/opioid_df_5.csv'


# converting csv 


opioid_prescriptions_tn = pd.read_csv(url2)
opioid_deaths_yearly_trend_tn = pd.read_csv(url1)

df4 = pd.read_csv(url_mp_q4)
opioid_df_5 =pd.read_csv(url_mp_q5)
df= pd.read_csv('opioid_zip_codes.csv')

# start of the application visuals
# question 1
st.header('question 1')
st.subheader('Which Tennessee counties had a disproportionately high number of opioid prescriptions?')



# question 2
st.header('question 2')
st.subheader('Who are the top opioid prescribers for the state of Tennessee?')
#Ui for filtering
# sort variables
sorted_unique_drugs = sorted(df.drug_name.unique())
# create sidebar
selected_drug = st.sidebar.multiselect('Question 2 Drugs filter', sorted_unique_drugs,default="METHADONE HCL")

# function where it filters by selections
df_selected_drugs = df[df.drug_name.isin(selected_drug)]

q2_treefig = px.treemap(df, path=['nppes_provider_zip5', 'drug_name'], values='total_claim',hover_data =['City'])
q2_treefig


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
# question 4
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

# question 5
st.header('question 5')
st.subheader('Is there any association between a particular type of opioid and number of overdose deaths?')

sorted_unique_opioid = sorted(opioid_df_5.opioid.unique())
selected_opioid = st.sidebar.multiselect('Question 5 drug filter', sorted_unique_opioid,default='codeine')

df_5_selected = opioid_df_5[opioid_df_5.opioid.isin(selected_opioid)]

q5_fig = px.scatter(df_5_selected, x="total_claims", y="overdose_deaths", size='population', color='opioid_percent',
           hover_name="county", size_max=20, trendline='ols', trendline_color_override='orange')
q5_fig