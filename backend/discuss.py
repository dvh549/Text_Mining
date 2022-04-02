
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
toxic_only_train_shortlisted = pd.read_pickle('../../Pre-Processed Files/toxic_only_train_shortlisted_preprocessed.pkl')
X = toxic_only_train_shortlisted["preprocessed_text"]
y = toxic_only_train_shortlisted["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
global tfidf_vec
tfidf_vec = TfidfVectorizer(ngram_range=(1,2), max_features=30000)
tfidf_train = tfidf_vec.fit_transform(X_train)

##Topic Extraction Task 2
global lda_preprocessed_comments
lda_preprocessed_comments = toxic_only_train_shortlisted['preprocessed_text'].map(lda_preprocess)
global dictionary
dictionary = corpora.Dictionary(lda_preprocessed_comments)

dictionary.filter_extremes(no_below=10, no_above=0.5, keep_n=75000)
global bow_corpus 
bow_corpus = [dictionary.doc2bow(doc) for doc in lda_preprocessed_comments]
# global lda_model
# lda_model = models.LdaMulticore(bow_corpus, num_topics=14,id2word=dictionary, passes=2, workers=2)

# @app.route('/', methods=['POST'])
# def createMsg():
#     data = {"count":0, "keywords":''}
#     try:
#         string = "Topic"
#         for i in range(0, 14):
#             new_String = string + str(i)
#             doc_ref = db.collection("DisabilityTopic").document(new_String)
#             doc_ref.set(data)
#         return jsonify(
#                 {
#                     "code": 200,
#                     "message": "success"
#                 }
#             ), 200 
#         ##
#     except Exception as e:
#         return jsonify(
#                 {
#                     "code": 500,
#                     "message": "sever error"
#                 }
#             ), 500

# @app.route('/classifyTopic', methods=['POST'])
# def classifyTopic():
#     try:
#         data = request.get_json()
#         print(data)
#         with open(r'C:\Users\wei-d\Documents\Y3S2\TextMining\Project\TM_Models\logreg_model.pkl' , 'rb') as f:
#             lr = pickle.load(f)
#         sent = data["sent"]
        
#         pred_val = tfidf_vec.transform([sent])
#         result = lr.predict(pred_val)
#         # print(result[0])
#         return jsonify (
#                 {
#                     "code": 200,
#                     "message": result[0]
#                 }
#             ), 200
#     except:
#         return jsonify(
#                 {
#                     "code": 500,
#                     "message": "sever error"
#                 }
#             ), 500

# @app.route('/getTopic', methods=['POST'])
# def getTopic():
#     try:
#         data = request.get_json()
#         sent= data["sent"]
#         processed_val = lda_preprocess(sent)
#         sent_data = [dictionary.doc2bow(doc) for doc in [processed_val]]
#         lda_model =  models.LdaModel.load(r'C:\Users\wei-d\Documents\Y3S2\TextMining\Project\LDA Model Files\lda_model.model')
#         merged = get_dominant_topics(lda_model, lda_model[sent_data], pd.Series([processed_val]))
#         dominate_topic = str(merged.iloc[0, 1])
#         perc_contribute = str(merged.iloc[0,2])
#         keywords = str(merged.iloc[0, 3])
#         result = {"dominate_topic":dominate_topic, "perc_cont":perc_contribute, "keywords":keywords}
        
#         return jsonify (
#                 {
#                     "code": 200,
#                     "message": result
#                 }
#             ), 200
#     except Exception as e:
#         return jsonify(
#                 {
#                     "code": 500,
#                     "message": e
#                 }
#             ), 500

@app.route('/orchestrator', methods=['POST'])
def orchestrator():
    try:
        data = request.get_json()
        print(data)
        with open(r'C:\Users\wei-d\Documents\Y3S2\TextMining\Project\TM_Models\logreg_model.pkl' , 'rb') as f:
            lr = pickle.load(f)
        sent = data["sent"]  
        pred_val = tfidf_vec.transform([sent])
        task_1_result = lr.predict(pred_val)
        processed_val = lda_preprocess(sent)     
        sent_data = [dictionary.doc2bow(doc) for doc in [processed_val]]
        lda_model =  models.LdaModel.load(r'C:\Users\wei-d\Documents\Y3S2\TextMining\Project\LDA_model2\LDA_model.model')
        merged = get_dominant_topics(lda_model, lda_model[sent_data], pd.Series([processed_val]))
        dominate_topic = str(merged.iloc[0, 1])
        perc_contribute = str(merged.iloc[0,2])
        keywords = str(merged.iloc[0, 3])
        task_2_result = {"dominate_topic":dominate_topic, "perc_cont":perc_contribute, "keywords":keywords}
        doc_ref = db.collection(task_1_result[0]).document()
        doc_ref.set(data)
        print(dominate_topic)
        doc_ref2 = db.collection(task_1_result[0]+"Topic").document("Topic"+dominate_topic)
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
