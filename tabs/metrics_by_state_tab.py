from streamlit.delta_generator import DeltaGenerator
import streamlit as st
import plotly.express as px


def get_filters(df, plot_col: DeltaGenerator):

    state = plot_col.selectbox("Select state", set(df.state_name))

    categories = plot_col.multiselect(
        "Choose categories", set(df.category),  ["Total"]
    )

    update = plot_col.button('filter')

    if "state" not in st.session_state:
        update = True
        st.session_state["state"] = True

    return state, categories, update


def main(tab_ref: DeltaGenerator, df):
    plot_col = tab_ref.columns(1)[0]

    state, categories, update = get_filters(df, plot_col)

    if update:
        data = df[df.state_name == state]
        data = data[data.category.isin(categories)]

        st.session_state["state_data"] = data

    if not categories:
        tab_ref.error("Please select at least one category.")
    else:

        tab_ref.write("### IDH by category")
        tab_ref.write(st.session_state["state_data"].sort_index())

        plot = px.line(st.session_state["state_data"], x="year",
                       y="value", color="category", markers=True)

        plot_col.plotly_chart(plot, use_container_width=True)
