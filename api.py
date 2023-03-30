from flask import Flask, request, jsonify
import pandas as pd
import pickle
from lime import lime_tabular
import numpy as np
import json
import re

# On récupère les données et on configure l'API
#data = pd.read_csv('/data/example_data.csv')
#train_data = pd.read_csv('/data/data_train.csv')
#my_pipeline = pickle.load(open("/data/pipeline_roc.pkl","rb"))
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
# API si aucune requête n'est entré
def home():
 return "<h1>Distant Reading Archive</h1><p>Bonjour. Veuiller faire une requête.</p>"
"""
# test local :http://127.0.0.1:5000/id_score/?SK_ID_CURR=100043
@app.route('/id_score/')
# Renvoie si le client a été autorisé à faire son crédit ou non
# Prend SK_ID_CURR pour identifier le client
# Renvoie -1 si le client n'est pas dans la base de données
def get_score():
 id = int(request.args.get('SK_ID_CURR'))
 id_data = data[data['SK_ID_CURR']==id]
 if(id_data.shape[0]==1):
  prediction = int(my_pipeline.predict(id_data.drop(["SK_ID_CURR",'TARGET'], axis=1))[0])
 else:
  prediction = -1

 return jsonify({'score':prediction})

# test local :http://127.0.0.1:5000/id_local_params/?SK_ID_CURR=100043&NB_FEATURE=5
@app.route('/id_local_params/')
# Renvoie si l'explication des caractéristiques du client et s'il a été autorisé ou non à faire son crédit
# Prends SK_ID_CURR pour identifier le client et NB_FEATURE pour décider du nombre de features à afficher
def get_local_params():
 id = int(request.args.get('SK_ID_CURR'))
 nb = int(request.args.get('NB_FEATURE'))
 classe = ['Crédit accordé', 'Crédit refusé']
 explainer = lime_tabular.LimeTabularExplainer(np.array(train_data), mode="classification",
                                               class_names=classe,
                                               feature_names=list(train_data.columns.values)
                                               )
 id_data = data[data['SK_ID_CURR'] == id]
 if(id_data.shape[0]==1):
    id_data_np = np.array(id_data.drop(["SK_ID_CURR",'TARGET'], axis=1))[0]
    explanation = explainer.explain_instance(id_data_np, my_pipeline.predict_proba,num_features=nb)
    pred = my_pipeline.predict(id_data.drop(["SK_ID_CURR",'TARGET'], axis=1))[0]
    return jsonify({'local_weight': explanation.as_html(),
                    'prediction':pred})
 else:
    explanation = -1
    return jsonify({'local_weight': explanation})

# test local : http://127.0.0.1:5000/id_global_params/
@app.route('/id_global_params/')
# Renvoie le poids de chaque caractéristique dans le modèle
# Renvoie la liste des caractéristiques
def get_global_params():
 lr = my_pipeline.best_estimator_.named_steps['classification']
 feature = train_data.columns.values
 return jsonify({'global_weight': list(lr.coef_[0]),
                 'feature':list(feature)})

# test local :http://127.0.0.1:5000/id_data_needed/?SK_ID_CURR=100043&NB_FEATURE=5
@app.route('/id_data_needed/')
# Cherche les caractéristiques les plus importantes du client pour la décision
# Renvoie les données des autres clients pour ses caractéristiques
# Fait un dataframe pour les clients refusés et un dataframe pour les clients acceptés
# Prends SK_ID_CURR pour identifier le client et NB_FEATURE pour décider du nombre de features à afficher
def get_data_with_params():
 id = int(request.args.get('SK_ID_CURR'))
 nb = int(request.args.get('NB_FEATURE'))
 classe = ['Crédit accordé', 'Crédit refusé']
 explainer = lime_tabular.LimeTabularExplainer(np.array(train_data), mode="classification",
                                               class_names=classe,
                                               feature_names=list(train_data.columns.values)
                                               )
 id_data = data[data['SK_ID_CURR'] == id]
 if(id_data.shape[0]==1):
    data_acc = data[data['TARGET'] == 0]
    data_ref = data[data['TARGET'] == 1]
    id_data_np = np.array(id_data.drop(["SK_ID_CURR",'TARGET'], axis=1))[0]
    explanation = explainer.explain_instance(id_data_np, my_pipeline.predict_proba,num_features=nb)
    # Les feature ne sont pas renvoyé directement par l'explainer. Il faut extraire une liste utilisable
    feature = []
    for i in explanation.as_list():
        if len(re.split('>|<', i[0])) == 2:
            feature.append(re.split('>|<', i[0])[0].strip())
        else:
            feature.append(re.split('>|<', i[0])[1].strip())
    return jsonify({'data_acc': data_acc[feature].to_json(orient='records'),
                    'data_ref': data_ref[feature].to_json(orient='records'),
                    'id_data':id_data.to_json(orient='records')})
 else:
    return jsonify({'data_acc': -1,
                    'data_ref':-1})
"""
if __name__=='__main__':
    app.run(debug=True)