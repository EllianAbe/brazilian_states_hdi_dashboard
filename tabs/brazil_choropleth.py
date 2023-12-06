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
    min = df.value.min()
    min = min - (min % 100)

    max = df.value.max()
    max = max + 100 - (max % 100)

    fig = px.choropleth(df,
                        geojson=get_geojson(),
                        locations='acronym',
                        color='value',
                        range_color=(min, max),
                        color_continuous_scale='Blues',
                        hover_name='state_name',
                        hover_data=['value'])

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        geo=dict(
            lataxis={'range': [-60, 10]},
            lonaxis={'range': [-100, -30]}
        ),
        height=600
    )

    fig.update_geos(fitbounds="geojson", visible=False)

    return fig


def main(tab: DeltaGenerator, df: pd.DataFrame):

    col1, col2 = tab.columns([1, 3])
    year = col1.select_slider('Year', df.year.unique())
    category = col1.selectbox('Category', df.category.unique())

    col2.header(f'HDI {year}: {category}')

    my_bar = col2.progress(0, text='Filtering data')
    df = df[(df.year == year) & (df.category == category)]

    my_bar.progress(50, 'Ploting figure')
    fig = plot(df)

    col2.plotly_chart(fig, use_container_width=True)

    my_bar.empty()
    tab.write(df)
