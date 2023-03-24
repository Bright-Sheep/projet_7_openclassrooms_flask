import streamlit as st
import requests
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Hello",
    page_icon="📈",
)
st.markdown("# Importance des caractéristiques globales")
st.markdown("Quel est le poid des caractéristiques dans le modèle utilisé.")


url = 'http://127.0.0.1:5000/id_global_params/'

weight = requests.get(url).json()["global_weight"]
feature = requests.get(url).json()["feature"]

with plt.style.context("ggplot"):
    fig = plt.figure(figsize=(8,12))
    plt.barh(range(len(weight)), weight, color=["red" if coef<0 else "green" for coef in weight])
    plt.yticks(range(len(weight)), feature);
    plt.title("Poids des caractéristiques")
st.pyplot(fig)