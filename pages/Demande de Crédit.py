import streamlit as st
import requests

st.set_page_config(
    page_title="Quick reference",  # => Quick reference - Streamlit
    page_icon="🐍",
    layout="centered",  # wide
    initial_sidebar_state="auto")  # collapsed

st.markdown("# Importance des caractéristiques locales")

st.sidebar.markdown(f"""
    # Paramètres
    """)

if 'my_params_1' not in st.session_state:
    st.session_state.my_params_1 = 5
if 'my_id_1' not in st.session_state:
    st.session_state.my_id_1 = 100043

nb_params = st.sidebar.slider('Sélectionner le nombre de paramètres à afficher', 1, 20, st.session_state.my_params_1)
st.session_state.my_params_2 = nb_params

id_client = st.sidebar.number_input('Id du client',min_value=0,value=st.session_state.my_id_1)
st.session_state.my_id_2 = id_client

url = f'http://127.0.0.1:5000/id_local_params/?SK_ID_CURR={id_client}&NB_FEATURE={nb_params}'
response = requests.get(url).json()["local_weight"]

if response != -1:
    st.components.v1.html(response, width=1100, height=1000, scrolling=True)
else :
    st.text('Client non trouvé. Veuillez le rajouter à la base de données.')