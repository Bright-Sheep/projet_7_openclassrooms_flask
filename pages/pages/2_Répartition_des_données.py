import streamlit as st
import requests
import json
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Répartition", page_icon="📈")

# On initialise les paramètres globaux au cas où on recharge la page
if 'my_params_2' not in st.session_state:
    st.session_state.my_params_2 = 5
if 'my_id_2' not in st.session_state:
    st.session_state.my_id_2 = 100043

# Titre de la page
st.markdown("# Répartition des caractéristiques locales")

st.markdown("Comment vous situez-vous par rapport aux autres clients ?")
# Barre latérale
st.sidebar.markdown(f"""
    # Paramètres
    """)
nb_params = st.sidebar.slider('Sélectionner le nombre de paramètres à afficher', 1, 20, st.session_state.my_params_2)
st.session_state.my_params_1 = nb_params

id_client = st.sidebar.number_input("Sélectionnez l'ID du client",min_value=0,value=st.session_state.my_id_2)
st.session_state.my_id_1 = id_client

# On fait la requête à l'url
url = f'http://127.0.0.1:5000/id_data_needed/?SK_ID_CURR={id_client}&NB_FEATURE={nb_params}'

# On sélectionne si on veut les données des crédits refusés ou acceptés
direction = st.radio('Selectionner une comparaison :', ('Crédit accepté','Crédit refusé'))
if direction == 'Crédit accepté':
    response = requests.get(url).json()["data_acc"]
else :
    response = requests.get(url).json()["data_ref"]

# On vérifie que la requête a donné un résultat et on affiche les graphiques
if response != -1:
    data_client =requests.get(url).json()["id_data"]
    client_json = json.loads(data_client)
    client_id = pd.json_normalize(client_json)

    response_json = json.loads(response)
    df = pd.json_normalize(response_json)
    feature = df.columns.values
    l = len(feature)
    fig, axes = plt.subplots(l, 1, figsize=(7, 2 * l), tight_layout=True)
    j = 0
    for f in feature:
        ax = axes[j]
        sns.histplot(df[f], kde=True, ax=ax)
        y = ax.lines[0].get_ydata()
        max_height = max(y)
        ax.set_title(f)
        ax.set_xticks([])
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.plot([client_id[f], client_id[f]], [0, max_height], color='red',linewidth=3.5)
        j += 1

    st.pyplot(fig)
else :
    st.text('Client non trouvé. Veuillez le rajouter à la base de données.')