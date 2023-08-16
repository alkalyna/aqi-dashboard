import pandas as pd
import pickle
import plotly.express as px 
import plotly.graph_objects as go
import streamlit as st
from PIL import Image


# Membuat Pengaturan App
APP_TITLE = 'Dashboard Air Quality Index (AQI)'
APP_SUB_TITLE = 'Source : https://www.kaggle.com/datasets/adityaramachandran27/world-air-quality-index-by-city-and-coordinates. Disclaimer : Data ini didapatkan dari Kaggle Datasets. Data AQI tidak menunjukan data realtime.'

st.set_page_config(APP_TITLE, page_icon=":bar_chart:", layout='wide')
st.title(APP_TITLE)
st.caption(APP_SUB_TITLE)

# Memasukkan gambar logo di sidebar
logo = Image.open("asset\yuksinau v1.png")
st.sidebar.image(logo)


# Caption di sidebar
st.sidebar.write('Hello everyone, perkenalkan saya Rifqi seorang _data analysis enthusiast_. Data Air Quality Index dibuat menggunakan Python dan diterapkan menjadi dashboard web app.')
st.sidebar.caption('Thank you for visiting this page. You can reach me on instagram @rifqistory or Linkedin.com/in/mrifqiabdr')

# Penjelasan AQI
st.header('Apa itu Air Quality Index?')
st.write(
    'Air Quality Index (AQI) adalah pengukuran konsentrasi polutan udara dalam polusi udara ambien dan risiko kesehatan yang terkait. Ada enam polutan udara yang diukur dalam rumus indeks, antara lain: PM2.5, PM10, karbon monoksida, sulfur dioksida, nitrogen dioksida, ozon permukaan tanah. Angka AQI ditetapkan berdasarkan polutan udara dengan angka AQI tertinggi pada saat kualitas udara diukur (dikutip dari iqair.com).'
    )

# Membuka file pickle
with open('df_use.pickle', 'rb') as f:
    data = pickle.load(f)

# Transformasi data
bar_data = data[['Country','City','AQI Category','AQI Value','CO AQI Value','Ozone AQI Value','NO2 AQI Value','PM2.5 AQI Value']]
pie_data = data.groupby(by=["Country", "AQI Category"], as_index=False).agg({"City": "count"})
largest = data.groupby(by=["Country"], as_index=False).agg({"City": "count"}).nlargest(5, columns='City')


# Exploratory Data Analysis
st.header('Exploratory Data Analysis')

fig_his = px.histogram(data, x="AQI Value", color='AQI Category',color_discrete_map={
                 "Good" : "#CAF0F8",
                 "Moderate" : "#90E0EF",
                 "Unhealthy for Sensitive Groups" : "#48CAE4",
                 "Unhealthy" : "#00B4D8",
                 "Very Unhealthy" : "#0077B6",
                 "Hazardous" : "#03045E"},
                 title="Distribusi Data Air Quality Index")
fig_his.update_layout(legend=dict(font=dict(size=10),orientation="h",yanchor="bottom",y=1,xanchor="right",x=1),
                  title=dict(x=0, y=0.98, font=dict(size=20)))

fig_largest = px.bar(largest, x='Country', y='City', title='Top 5 Country Data Sample')
fig_largest.update_layout(title=dict(font=dict(size=20)))

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_his, theme=None, use_container_width=True)
with col2:
    st.plotly_chart(fig_largest, theme=None, use_container_width=True)

# Membuat Sebaran Peta
map = px.scatter(data, x="lng", y="lat", title='Sebaran Air Quality Index', color='AQI Category', color_discrete_map={
                 "Good" : "#CAF0F8",
                 "Moderate" : "#90E0EF",
                 "Unhealthy for Sensitive Groups" : "#48CAE4",
                 "Unhealthy" : "#00B4D8",
                 "Very Unhealthy" : "#0077B6",
                 "Hazardous" : "#03045E"})
map.update_layout(title=dict(font=dict(size=20)),
                  xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

st.plotly_chart(map, theme=None, use_container_width=True)

# Membuat Filter Selectbox
country_list = list(bar_data['Country'].value_counts().keys().sort_values())
country = st.selectbox(label='Select Country', options=country_list)
    
if country:
    bar_data = bar_data[bar_data['Country'] == country]
    pie_data = pie_data[pie_data['Country'] == country]
    

# Analisa per negara    
st.header(f'AQI Value of {country}')

# Membuat metric / kartu / KPI
metric_title_avg = f'Avg of AQI Value'
avg = bar_data['AQI Value'].mean()

metric_title_median = f'Median of AQI Value'
median = bar_data['AQI Value'].median()

metric_title_max = f'Max of AQI Value'
max = bar_data['AQI Value'].max()

metric_title_min = f'Min of AQI Value'
min = bar_data['AQI Value'].min()


# Membagi metric pada kolom-kolom
col1, col2, col3, col4 = st.columns(4)
with col1: 
    st.metric(metric_title_avg, '{:.2f}'.format(avg))
with col2:
    st.metric(metric_title_median, median)
with col3:
    st.metric(metric_title_max, max)
with col4:
    st.metric(metric_title_min, min)

# Membuat Pie Chart
fig_pie = px.pie(pie_data, values='City', names='AQI Category', 
             color='AQI Category',color_discrete_map={
                 "Good" : "#CAF0F8",
                 "Moderate" : "#90E0EF",
                 "Unhealthy for Sensitive Groups" : "#48CAE4",
                 "Unhealthy" : "#00B4D8",
                 "Very Unhealthy" : "#0077B6",
                 "Hazardous" : "#03045E",
             },
             title=f'Percentage AQI Value of City in {country}',
             )
fig_pie.update_layout(title=dict(x=0, y=0.9, font=dict(size=20)))
st.plotly_chart(fig_pie, theme=None, use_container_width=True)

aqi_list = [""] + list(bar_data['AQI Category'].value_counts().keys().sort_values())
aqi_category = st.selectbox(label='Select AQI Category', options=aqi_list)

if aqi_category:
    bar_data = bar_data[bar_data['AQI Category'] == aqi_category]

# Membuat bar chart
fig_bar = px.bar(bar_data, x='AQI Value', y='City', color='AQI Category',             
             hover_data=['CO AQI Value','Ozone AQI Value','NO2 AQI Value','PM2.5 AQI Value'],
             title= f"AQI Value of City in {country}",
             orientation='h',text_auto=True,
             color_discrete_map={
                 "Good" : '#CAF0F8',
                 "Moderate" : '#90E0EF',
                 "Unhealthy for Sensitive Groups" : '#48CAE4',
                 "Unhealthy" : '#00B4D8',
                 "Very Unhealthy" : '#0077B6',
                 "Hazardous" : '#03045E'}
             )
fig_bar.update_layout(yaxis={'categoryorder':'total ascending'},
                  height=900,
                  legend=dict(font=dict(size=10),orientation="h",yanchor="bottom",y=1,xanchor="right",x=1),
                  title=dict(x=0, y=0.98,
                             font=dict(size=20)))

st.plotly_chart(fig_bar, theme=None, use_container_width=True, height=950)

# Membuat expander di tabel data
with st.expander("See The Data Table"):
    st.write(f"Berikut adalah data Air Quality Index 'AQI' kota-kota yang ada di {country}")
    st.write(bar_data.shape)
    st.dataframe(bar_data)
    

