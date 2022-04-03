
from itertools import count
from tempfile import TemporaryFile
import firebase_admin
from firebase_admin import credentials, firestore, auth
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime,timedelta
import pandas as pd
import pickle
import os 
from invokes import invoke_http
import numpy as np

cred = credentials.Certificate("secretKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__) 
CORS(app)

@app.route("/",methods=["POST"])
def createMovieReview():
    try:
        toxic_only_train_shortlisted = pd.read_pickle('../../Pre-Processed Files/toxic_only_train_shortlisted_preprocessed.pkl')
        x = toxic_only_train_shortlisted["preprocessed_text"]
        for index, value in x[:1000,].items():
            invoke_http('http://127.0.0.1:5000/orchestrator', method="POST", json= {"sent":value})
            # print(value)
        return jsonify(
            {
                "code": 200,
                "message":"success"
            }
        ),200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": e
            }
        ),500    



if __name__ == '__main__':
    # app.run(host="0.0.0.0",port=5000, debug=True)
    app.run(port=5001, debug=True)
