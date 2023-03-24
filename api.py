from flask import Flask, request, jsonify
import pandas as pd
import pickle
from lime import lime_tabular
import numpy as np
import json
import re

data = pd.read_csv('dashboard\example_data.csv').drop(['TARGET'],axis=1)
train_data = pd.read_csv('dashboard\data_train.csv')
my_pipeline = pickle.load(open("dashboard/pipeline_roc.pkl","rb"))
app = Flask(__name__)
app.config["DEBUG"] = True
@app.route('/')
def home():
 return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

# test local :http://127.0.0.1:5000/id_score/?SK_ID_CURR=100043
@app.route('/id_score/')
def get_score():
 id = int(request.args.get('SK_ID_CURR'))
 id_data = data[data['SK_ID_CURR']==id]
 if(id_data.shape[0]==1):
  prediction = int(my_pipeline.predict(id_data.drop(["SK_ID_CURR"], axis=1))[0])
 else:
  prediction = -1

 return jsonify({'score':prediction})

# test local :http://127.0.0.1:5000/id_local_params/?SK_ID_CURR=100043&NB_FEATURE=5
@app.route('/id_local_params/')
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
    id_data_np = np.array(id_data.drop(["SK_ID_CURR"], axis=1))[0]
    explanation = explainer.explain_instance(id_data_np, my_pipeline.predict_proba,num_features=nb)
    pred = my_pipeline.predict(id_data.drop(["SK_ID_CURR"], axis=1))[0]
    return jsonify({'local_weight': explanation.as_html(),
                    'prediction':pred})
 else:
    explanation = -1
    return jsonify({'local_weight': explanation})

# test local : http://127.0.0.1:5000/id_global_params/
@app.route('/id_global_params/')
def get_global_params():
 lr = my_pipeline.best_estimator_.named_steps['classification']
 feature = train_data.columns.values
 return jsonify({'global_weight': list(lr.coef_[0]),
                 'feature':list(feature)})

# test local :http://127.0.0.1:5000/id_data_needed/?SK_ID_CURR=100043&NB_FEATURE=5
@app.route('/id_data_needed/')
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
    id_data_np = np.array(id_data.drop(["SK_ID_CURR"], axis=1))[0]
    explanation = explainer.explain_instance(id_data_np, my_pipeline.predict_proba,num_features=nb)
    feature = []
    for i in explanation.as_list():
        if len(re.split('>|<', i[0])) == 2:
            feature.append(re.split('>|<', i[0])[0].strip())
        else:
            feature.append(re.split('>|<', i[0])[1].strip())
    return jsonify({'data': data[feature].to_json(orient='records'),
                    'id_data':id_data.to_json(orient='records')})
 else:
    return jsonify({'data': -1})

app.run()