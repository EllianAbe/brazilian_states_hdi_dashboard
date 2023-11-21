import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import pandas as pd
import plotly.express as px


@st.cache_data
def get_data():
    df = pd.read_csv('data.csv', sep=',')

    return df.set_index('no_uf')


def get_filters(df, plot_col: DeltaGenerator):

    state = plot_col.selectbox("Select state", set(df.index))

    categories = plot_col.multiselect(
        "Choose categories", set(df.idh_categoria),  ["Total"]
    )

    update = plot_col.button('filter')

    if "startup" not in st.session_state:
        update = True
        st.session_state["startup"] = True

    return state, categories, update


# Page setting
st.set_page_config(layout="wide", page_title="States IDH")


st.tabs(['state', 'comparision'])

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

df = get_data()

plot_col = st.columns(1)[0]

state, categories, update = get_filters(df, plot_col)

if update:
    data = df.loc[state]
    data = data[data.idh_categoria.isin(categories)]

    st.session_state["data"] = data


if not categories:
    st.error("Please select at least one category.")
else:

    st.write("### IDH by category", st.session_state["data"].sort_index())

    plot = px.line(st.session_state["data"], x="ano",
                   y="valor", color="idh_categoria", markers=True)

    plot_col.plotly_chart(plot, use_container_width=True)
