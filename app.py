import streamlit as st

st.title("Meine erste App!")
st.write("Hallo Welt!")

name = st.text_input("Wie heißt du?")
if name:
    st.write(f"Willkommen, {name}!")