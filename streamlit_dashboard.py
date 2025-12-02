import streamlit as st
import pandas as pd
import plotly.express as px
import glob
import os

st.set_page_config(page_title="Monitoraggio Certificati Accredia", layout="wide")

# Carica tutti i CSV dalla cartella
csv_files = glob.glob("accredia_data/*.csv")
dfs = []
for file in csv_files:
    ente = os.path.basename(file).split("_")[0]
    df = pd.read_csv(file)
    df['ente'] = ente
    df['data'] = pd.to_datetime(file.split("_")[1].replace(".csv", ""))
    dfs.append(df)
data = pd.concat(dfs)

# Sidebar per selezione enti e periodo
enti = st.sidebar.multiselect("Seleziona enti", options=data['ente'].unique(), default=list(data['ente'].unique()))
data = data[data['ente'].isin(enti)]
date_min, date_max = data['data'].min(), data['data'].max()
date_range = st.sidebar.slider("Periodo", min_value=date_min, max_value=date_max, value=(date_min, date_max))
data = data[(data['data'] >= date_range[0]) & (data['data'] <= date_range[1])]

# Grafico interattivo
fig = px.line(data, x='data', y='certificati_attivi', color='ente', markers=True,
              labels={'certificati_attivi': 'Certificati attivi', 'data': 'Data'})
st.plotly_chart(fig, use_container_width=True)

# Statistiche riassuntive
st.write("Statistiche riassuntive:")
st.dataframe(data.groupby('ente')['certificati_attivi'].agg(['min', 'max', 'mean', 'last']))

# Download dati filtrati
st.download_button("Scarica dati filtrati", data.to_csv(index=False), "dati_filtrati.csv")
