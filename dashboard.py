import pandas as pd
import streamlit as st

st.title('N2 verkeersdrukte')

# df = pd.read_csv('stukjen2_vr.csv', sep=';', decimal='.')
df = pd.read_excel('n2_final.xlsx')
df = df.set_index('tijd')

df.rename(
    columns={
        'Latitude':'lat',
        'Longitude':'lon',
    }, inplace=True)

df.index.name = 'index'
df['lus'] = df['lus'].apply(lambda x: x[4:] if not 'MONIBAS' in x else x[18:])

lus = st.sidebar.selectbox('Selecteer verkeerslus', df['lus'].unique())

day = st.sidebar.slider(label='Selecteer dag v/d week', min_value=0,
                        max_value=6)
days = ['ma', 'di', 'wo', 'do', 'vr', 'za', 'zo']

day_filtered = df.loc[df['dag van de week'] == days[day]]

lus_filtered = day_filtered.loc[day_filtered['lus'] == lus]

nonlussen = df.loc[df['lus'] != lus]
lussie = df.loc[df['lus'] == lus]

st.deck_gl_chart(
    viewport={
        'latitude': nonlussen.groupby('lus').first()['lat'][2],
        'longitude': nonlussen.groupby('lus').first()['lon'][2],
        'zoom': 12,
        'pitch': 50,
    },
    layers=[
        {
        'data': nonlussen.groupby('lus').first(),
        'type': 'ScatterPlotLayer',
        'radius': 100
        },
        {
        'data': lussie.groupby('lus').first(),
        'type': 'ScatterPlotLayer',
        'radius': 300,
        'getColor': [75,205,250]
        },
    ])

st.bar_chart(lus_filtered['Intensiteit'])
st.bar_chart(lus_filtered['Gemiddelde snelheid'])


