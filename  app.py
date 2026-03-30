import streamlit as st

st.title("Meine erste App!")
st.write("Hallo Welt! Das ist meine erste Streamlit App.")

name = st.text_input("Wie heißt du?")
if name:
    st.write(f"Willkommen, {name}!")