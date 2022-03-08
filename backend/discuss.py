
from tempfile import TemporaryFile
import firebase_admin
from firebase_admin import credentials, firestore, auth
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime,timedelta

import os 

cred = credentials.Certificate("secretKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__) 
CORS(app)

@app.route('/', methods=['POST'])
def createMsg():
    print("here")
    data = request.get_json()
    datetime_now = datetime.now()
    curr_datetime = (datetime_now).strftime("%m/%d/%Y, %H:%M:%S")
    data["timestamp"] = curr_datetime
    data["raw_timestamp"] = datetime_now
    try:
        doc_ref = db.collection("discussMsg").document()
        doc_ref.set(data)
        #validate then return error code#######
        return jsonify(
                {
                    "code": 200,
                    "message": "success"
                }
            ), 200 
        ##
    except Exception as e:
        return jsonify(
                {
                    "code": 500,
                    "message": "sever error"
                }
            ), 500



if __name__ == '__main__':
    # app.run(host="0.0.0.0",port=5000, debug=True)
    app.run(port=5000, debug=True)
