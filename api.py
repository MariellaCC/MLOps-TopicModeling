import uvicorn 
import gensim
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
from nltk.corpus import stopwords
from fastapi import FastAPI, Depends, HTTPException, status, Header, Path
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import pandas as pd 
import numpy as np 
from gensim.test.utils import datapath
from ast import literal_eval
from gensim import corpora
import os
import re 
from sqlalchemy import URL, create_engine, inspect, text
from data_ingestion import read_txt_content, get_date, get_ref, get_files_list, preprocess_data
from pre_processing import load_data,tokenize_documents, preprocess_tokens, load_stopwords, remove_stopwords, create_bigrams, save_dataframe
from kpi import load_corpus_model, preprocess_data_kpi, load_lda_model, calculate_coherence, compute_perplexity
import nltk 
import duckdb
import secrets
from typing import Annotated
import mysql.connector
import api_modules
import datetime


nltk.download('punkt')
nltk.download('stopwords')

import nltk
from sqlalchemy import create_engine
import mysql.connector

nltk.download('punkt')
nltk.download('stopwords')

url_object = URL.create(
    "mysql+pymysql",
    username="root",
    password="password",
    host="tm_db",  # Use the service name defined in docker-compose.yml
    #host="localhost",  # Use the service name defined in docker-compose.yml
    port=3306,     # Use the MySQL container's exposed port
    database="DB",
)
engine = create_engine(url_object)

connection = mysql.connector.connect(
    user="root",
    password="password",
    host="tm_db",  # Use the service name defined in docker-compose.yml
    #host="localhost",  # Use the service name defined in docker-compose.yml
    port=3306,     # Use the MySQL container's exposed port
    database="DB"
)

app = FastAPI()
security = HTTPBasic()

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"admin"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"mdp"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

#class topic(BaseModel):
#    num_topic: int = 2
#    date_ref_1 :str = "1930-06-06"
#    date_ref_2 : str = "1931-05-01"

class database(BaseModel):
    file_name: str = 'test_file'
    file_content: str = 'Mattia è un bimbo di 5 anni che passa tutte le sue giornate a disegnare. In realtà Mattia non si impegna più del necessario per tratteggiare le linee, fare bene le forme o rendere somiglianti le persone che disegna. Mattia ama soprattutto colorare, e ad ogni persona o cosa che disegna associa dei colori specifici. Ogni qual volta disegna suo papà Giuseppe, ad esempio, usa sempre gli stessi colori: i capelli li fa in nero, la maglia è azzurra e i pantaloni rigorosamente rossi. Il papà di Mattia non si veste ovviamente con colori così sgargianti, ma a Mattia piace immaginarlo così.'
    date: str = '2001'
    publication_name: str = 'test'
    publication_ref: str = 'test'
    num_topic: int = 2

class read_db(BaseModel):
    file_name: str = 'test_file'
 


@app.get('/')
def Say_hello():
    """Vérifie que l'API fonctionne"""
         
    return "Hello, I'm working"




#@app.post('/topic')
#def get_topic(topic:topic,username: Annotated[str, Depends(get_current_username)]):
#    #data ingestion
#    
#    #subset_df = preprocess_data(folder_name, pub_refs, pub_names, topic.date_ref_1, topic.date_ref_2)
#    #subset_df.to_csv('subset.csv')
#    query = text(f"SELECT * FROM sources WHERE date <= DATE '{topic.date_ref_2}' AND date > DATE '{topic.date_ref_1}'")
#    corpus_df = pd.read_sql_query(query, engine) 
#    #pre process
#    #corpus_df = load_data('subset.csv')
#    corpus_df = tokenize_documents(corpus_df, 'file_content')
#    corpus_df = preprocess_tokens(corpus_df, 'tokens')
#    stopwords = load_stopwords('stop_words.csv')
#    corpus_df = remove_stopwords(corpus_df, 'doc_prep', stopwords)
#    # Create bigrams
#    corpus_df = create_bigrams(corpus_df, 'doc_prep_nostop')
#    # Save processed data
#    save_dataframe(corpus_df['bigrams'], 'corpus_model.csv')
#
#    #kpi
#
#    corpus_model_file = 'corpus_model.csv'
#    current_directory = os.getcwd()
#    lda_model_file = os.path.join(current_directory, 'lda_model')  # Construct the path to the LDA model file
#    bigrams = load_corpus_model(corpus_model_file)
#    #dans le fichier kpi il faut renommer la fonction preprocess_data en preprocess_date_kpi sinon elle porte le même nom que celle pour la data ingestion
#    id2word, corpus = preprocess_data_kpi(bigrams)
#    lda = load_lda_model(lda_model_file)
#
#    topic_print_model = lda.print_topics(num_words=topic.num_topic)
#    coherence_value = calculate_coherence(lda, bigrams, corpus, id2word)
#    dic = { topic_print_model[i][0] : topic_print_model[i][1]  for i in range (7)}
#    
#    return {'topic':dic, 'coherence':coherence_value}

@app.put('/topic')
def add_data_and_get_topic(database:database):
    cursor = connection.cursor()
    query2 = f"""INSERT INTO new_text (file_name,file_content,date,publication_name,publication_ref) VALUES ('{database.file_name}','{database.file_content}','{database.date}','{database.publication_name}','{database.publication_ref}')"""
    cursor.execute(query2)
    connection.commit()
    cursor.close()
    #return{cursor.rowcount: "Record inserted successfully into Laptop table"}
    
  
    query = text(f"SELECT * FROM new_text WHERE file_name = '{database.file_name}'")
    corpus_df = pd.read_sql_query(query, engine) 
    #pre process
    #corpus_df = load_data('subset.csv')
    corpus_df = tokenize_documents(corpus_df, 'file_content')
    corpus_df = preprocess_tokens(corpus_df, 'tokens')
    stopwords = load_stopwords('stop_words.csv')
    corpus_df = remove_stopwords(corpus_df, 'doc_prep', stopwords)
    # Create bigrams
    corpus_df = create_bigrams(corpus_df, 'doc_prep_nostop')
    # Save processed data
    save_dataframe(corpus_df['bigrams'], 'corpus_model.csv')

    #kpi

    corpus_model_file = 'corpus_model.csv'
    current_directory = os.getcwd()
    lda_model_file = os.path.join(current_directory, 'lda_model')  # Construct the path to the LDA model file
    bigrams = load_corpus_model(corpus_model_file)
    #dans le fichier kpi il faut renommer la fonction preprocess_data en preprocess_date_kpi sinon elle porte le même nom que celle pour la data ingestion
    id2word, corpus = preprocess_data_kpi(bigrams)
    lda = load_lda_model(lda_model_file)

    topic_print_model = lda.print_topics(num_words=database.num_topic)
    print(topic_print_model)
    coherence_value = calculate_coherence(lda, bigrams, corpus, id2word)
    print(coherence_value)
    #perplexity_score = compute_perplexity(lda, corpus)
    cursor = connection.cursor()
    query2 = f"""INSERT INTO metrics (file_name,timestamp,coherence,perplexity) VALUES ('{database.file_name}',"timestamp",'{coherence_value}',"5")"""
    cursor.execute(query2)
    connection.commit()
    cursor.close()

    dic = { topic_print_model[i][0] : topic_print_model[i][1]  for i in range(5)}
    
    return {'topic':dic, 'coherence':coherence_value}
    #return {'topic':dic, 'coherence':coherence_value,'perplexity':perplexity_score}

@app.post('/topic/metrics')
def get_metrics_from_publication(read_db:read_db):
    query = text(f"SELECT * FROM metrics WHERE file_name = '{read_db.file_name}'")
    with engine.connect() as conn:
        result = conn.execute(query)
    lis=[]
    for row in result:
        lis.append(row)
       
    test = ['file_name','timestamp','coherence']
    dic = { test[i] : lis[0][i]  for i in range(len(test))}
    return dic

@app.get('/doc/topics_probability')
def get_prob_from_publication():
    query = text(f"select * from sources LIMIT 5")
    with engine.connect() as conn:
        result = conn.execute(query)
    lis=[]
    #print(result)
    for row in result:
        print(row)
        lis.append(row)
    #test = ['file_name','timestamp','coherence']
    dic = { 'result': lis[0][5]}
    return dic

@app.put('/doc/update_model_metrics/{n}/')
def metrics_new_texts(n: Annotated[int, Path(description="Enter number of texts.")]):
    query = text(f"select * from new_text LIMIT {n}")
    with engine.connect() as conn:
        result = conn.execute(query)
    lis=[]
    for row in result:
        lis.append(row[5])
    
    lda_model = api_modules.load_lda_model('lda_model')
    id2word = 'lda_model.id2word'

    topics, perplexity, coherence, alert = api_modules.compute_metrics(lis,lda_model,id2word,threshold_coherence=0.38,threshold_perplexity=-10)

    now = str(datetime.datetime.now())

    cursor = connection.cursor()
    query2 = f"""INSERT INTO metrics (timestamp,coherence,perplexity) VALUES ({now},'{coherence}',{perplexity})"""
    cursor.execute(query2)
    connection.commit()
    cursor.close()

    dic = { 'topics': topics,
           'perplexity': perplexity,
           'coherence': coherence,
           'alert': alert}
    return dic