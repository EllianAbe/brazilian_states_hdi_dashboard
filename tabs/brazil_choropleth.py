import pandas as pd
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import plotly.express as px
import json


@st.cache_data
def get_geojson():
    with open('data/geodata.json') as response:
        geojson = json.load(response)

    return geojson


@st.cache_data
def get_data():
    df = pd.read_csv('data/report.csv')

    return df


@st.cache_data
def plot(df):
    min = df.valor.min()
    min = min - (min % 100)

    max = df.valor.max()
    max = max + 100 - (max % 100)

    fig = px.choropleth(df,
                        geojson=get_geojson(),
                        locations='sigla',
                        color='valor',
                        range_color=(min, max),
                        color_continuous_scale='Blues',
                        hover_name='no_uf',
                        hover_data=['valor'])

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        geo=dict(
            lataxis={'range': [-60, 10]},
            lonaxis={'range': [-100, -30]}
        ),
        height=650
    )

    fig.update_geos(fitbounds="geojson", visible=False)

    return fig


def main(tab: DeltaGenerator, df: pd.DataFrame):

    col1, col2 = tab.columns([1, 3])
    year = col1.select_slider('Year', df.ano.unique())
    category = col1.selectbox('Category', df.idh_categoria.unique())

    df = df[(df.ano == year) & (df.idh_categoria == category)]

    fig = plot(df)

    col2.header(f'HDI {year}: {category}')
    col2.plotly_chart(fig, use_container_width=True)

    tab.write(df)
