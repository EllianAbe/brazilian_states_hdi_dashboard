import streamlit as st
import pandas as pd
from tabs import metrics_by_state_tab, states_by_metric_tab


@st.cache_data
def get_data():
    df = pd.read_csv('data/report.csv', sep=',')

    return df

def main():
    state, comparision = st.tabs(['index by state', 'states by index'])

    df = get_data()

    metrics_by_state_tab.main(state, df)
    states_by_metric_tab.main(comparision, df)

# Page setting
st.set_page_config(layout="wide", page_title="States HDI")
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

main()