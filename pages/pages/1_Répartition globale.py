import streamlit as st
import requests
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
st.markdown("# Importance des caractéristiques globales")
st.sidebar.markdown(f"""
    # Paramètres
    """)
nb_params = st.sidebar.slider('Sélectionner le nombre de paramètres à afficher', 1, 20, st.session_state.my_params_2)
st.session_state.my_params_1 = nb_params

id_client = st.sidebar.number_input('Id du client',min_value=0,value=st.session_state.my_id_2)
st.session_state.my_id_1 = id_client

url = 'http://127.0.0.1:5000/id_global_params/'

weight = requests.get(url).json()["global_weight"]
feature = requests.get(url).json()["feature"]

with plt.style.context("ggplot"):
    fig = plt.figure(figsize=(8,12))
    plt.barh(range(len(weight)), weight, color=["red" if coef<0 else "green" for coef in weight])
    plt.yticks(range(len(weight)), feature);
    plt.title("Weights")
st.pyplot(fig)