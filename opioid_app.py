import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np

from sqlalchemy import create_engine

connection_prescribers = "postgres://postgres:postgres@localhost:5432/prescribers"
engine = create_engine(connection_prescribers)
query_spec = '''
SELECT 
	prescriber.specialty_description,
	SUM(prescription.total_claim_count) AS total_claim
FROM prescriber INNER JOIN prescription
ON prescriber.npi = prescription.npi
WHERE prescription.drug_name IN (
	SELECT drug_name
	FROM drug
	WHERE drug.opioid_drug_flag = 'Y'
	AND drug.drug_name='OXYCONTIN'
)
GROUP BY prescriber.specialty_description
ORDER BY total_claim DESC;
'''
result = engine.execute(query_spec)
query_city = '''
SELECT 
	prescriber.nppes_provider_city,
	SUM(prescription.total_claim_count) AS total_claim
FROM prescriber INNER JOIN prescription
ON prescriber.npi = prescription.npi
WHERE prescription.drug_name IN (
	SELECT drug_name
	FROM drug
	WHERE drug.opioid_drug_flag = 'Y'
	AND drug.drug_name='OXYCONTIN'
)
GROUP BY prescriber.nppes_provider_city
ORDER BY total_claim DESC;
'''

result = engine.execute(query_city)

prescribers = pd.read_sql(query_spec, con = engine)
city_opioid = pd.read_sql(query_city,con = engine)


st.header('question 1')
st.subheader('Who are the top opioid prescribers for the state of Tennessee?')

st.header('question 2')
st.subheader('Who are the top opioid prescribers for the state of Tennessee?')
st.dataframe(prescribers)
fig = px.bar(prescribers, x='total_claim', y='specialty_description',
title='Most prescribed Methodone by Specialty')
fig
st.dataframe(city_opioid)
fig1 = px.bar(city_opioid, x='total_claim', y='nppes_provider_city',
title='Most prescribed Methodone by City')
fig1


st.header('question 3')
st.subheader('Who are the top opioid prescribers for the state of Tennessee?')

st.header('question 4')
st.subheader('Who are the top opioid prescribers for the state of Tennessee?')

st.header('question 5')
st.subheader('Who are the top opioid prescribers for the state of Tennessee?')