
from itertools import count
from tempfile import TemporaryFile
from unittest import result
import firebase_admin
from firebase_admin import credentials, firestore, auth
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime,timedelta
import pandas as pd
import pickle
import os 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora, models
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pyLDAvis
import pyLDAvis.gensim_models
import numpy as np 
import operator
from joblib import load

cred = credentials.Certificate("secretKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__) 
CORS(app)

def lda_preprocess(text):
    result = []
    for token in simple_preprocess(text):
        if token not in STOPWORDS:
            result.append(token)
    return result

def get_dominant_topics(lda_model, tpd, texts):

    arr = []
    
    # Get main topic in each document
    for i, row_list in enumerate(tpd):
        row = row_list[0] if lda_model.per_word_topics else row_list            
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic (which is the first element in row), Perc Contribution and Keywords for each document
        dominant = row[0]
        topic_keywords = ", ".join([word for word, prop in lda_model.show_topic(dominant[0])])
        arr.append([int(dominant[0]), round(dominant[1], 4), topic_keywords])
        
    dominant_topics_df = pd.DataFrame(arr, columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords'], index=texts.index)
    merged = pd.concat([dominant_topics_df, texts], axis=1)
    merged.reset_index(inplace=True)
    merged.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
    
    return merged


## classification Task 1
toxic_only_train_shortlisted = pd.read_pickle('webAppDatasets/toxic_only_train_shortlisted_preprocessed.pkl')
X = toxic_only_train_shortlisted["preprocessed_text"]
y = toxic_only_train_shortlisted["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
global tfidf_vec
tfidf_vec = TfidfVectorizer(ngram_range=(1,2), max_features=30000)
tfidf_train = tfidf_vec.fit_transform(X_train)

##Topic Extraction Task 2
df = pd.read_csv('webAppDatasets/topic_keywords.csv')
topics={"topic1":' '.join(df.iloc[0,1:].to_numpy()),"topic2": " ".join(df.iloc[1,1:].to_numpy()),"topic3": " ".join(df.iloc[2,1:].to_numpy()), "topic4": " ".join(df.iloc[3,1:].to_numpy()), "topic5": " ".join(df.iloc[4,1:].to_numpy()), "topic6": " ".join(df.iloc[5,1:].to_numpy())  }


@app.route('/orchestrator', methods=['POST'])
def orchestrator():
    try:
        data = request.get_json()
        print(data)
        with open('webAppDatasets/logreg_model.pkl' , 'rb') as f:
            lr = pickle.load(f)
        sent = data["sent"]  
        pred_val = tfidf_vec.transform([sent])
        task_1_result = lr.predict(pred_val)
        count_vectorizer = CountVectorizer()
        lda_count_vecs = count_vectorizer.fit_transform([sent])
        
        lda_model = load('webAppDatasets/sklearn_lda.jl')
        for i in range(len([sent])):
            output = lda_model.fit_transform(lda_count_vecs[i])
            dominant_topic = np.argmax(output, axis=1)
            print("test doc" + str(i) + ": " + str(dominant_topic))
        dominant_topic = dominant_topic[0]
        print(dominant_topic)

        keywords =topics['topic'+str(dominant_topic+1)]
        task_2_result = {"dominate_topic":str(dominant_topic+1), "keywords": keywords}
        doc_ref = db.collection(task_1_result[0]).document()
        doc_ref.set(data)
        # print(dominant_topic)
        print("Topic"+str(dominant_topic+1))
        doc_ref2 = db.collection(task_1_result[0]+"Topic").document("Topic"+str(dominant_topic+1))
        doc = doc_ref2.get()
        # print(doc.to_dict())
        doc_data = doc.to_dict()
        doc_data["count"]+=1
        if keywords != doc_data["keywords"]:
            doc_data["keywords"] = keywords
        doc_ref2.update(doc_data)
        return jsonify (
                {
                    "code": 200,
                    "task1": task_1_result[0],
                    "task2":  task_2_result
                }
            ), 200
    except Exception as e:
        return jsonify(
                {
                    "code": 500,
                    "message": e
                }
            ), 500


@app.route('/getTopic', methods=['POST'])
def getTopic():
    try:
        result = []
        data = request.get_json()
        docs = db.collection(data['topic']+"Topic").stream()
        for doc in docs:
            doc_result = doc.to_dict()
            doc_result["topicID"] = doc.id
            result.append(doc_result)
        # print(result)
        result = sorted(result, key=operator.itemgetter('count'), reverse=True)
        # print(result)
        return jsonify (
                {
                    "code": 200,
                    "message": result
                }
            ), 200
    except Exception as e:
        return jsonify(
                {
                    "code": 500,
                    "message": e
                }
            ), 500

if __name__ == '__main__':
    # app.run(host="0.0.0.0",port=5000, debug=True)
    app.run(port=5000, debug=True)
