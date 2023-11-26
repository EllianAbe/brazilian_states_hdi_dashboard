from streamlit.delta_generator import DeltaGenerator
import streamlit as st
import plotly.express as px
import pandas as pd

def get_filters(df, plot_col: DeltaGenerator):

    states = plot_col.multiselect("Select states", set(df.no_uf), 
                                  ["São Paulo", "Rio de Janeiro", "Amazonas"])

    category = plot_col.selectbox(
        "Choose category", set(df.idh_categoria)
    )

    update = plot_col.button('Filter')

    if "comparision" not in st.session_state:
        update = True
        st.session_state["comparision"] = True

    return states, category, update

def main(tab_ref: DeltaGenerator, df: pd.DataFrame):
    plot_col = tab_ref.columns(1)[0]

    states, category, update = get_filters(df, plot_col)

    if update:
        data = df[df.no_uf.isin(states)]
        data = data[data.idh_categoria==category]

        st.session_state["comparision_data"] = data

    if not category:
        tab_ref.error("Please select at least one state.")
    else:

        tab_ref.write("### IDH by category")
        tab_ref.write(st.session_state["comparision_data"].sort_index())

        plot = px.line(st.session_state["comparision_data"], x="ano",
                    y="valor", color="no_uf", markers=True)

        plot_col.plotly_chart(plot, use_container_width=True)
