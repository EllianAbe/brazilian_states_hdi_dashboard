import streamlit as st

st.set_page_config(layout="centered", page_title="Login")
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

form = st.form("credentials")

form.header("Login")
username = form.text_input("Username")
password = form.text_input("Passowrd", type="password")
form.form_submit_button("Login")