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
from python_code.data_ingestion import read_txt_content, get_date, get_ref, get_files_list, preprocess_data
from python_code.pre_processing import load_data,tokenize_documents, preprocess_tokens, load_stopwords, remove_stopwords, create_bigrams, save_dataframe
from python_code.kpi import load_corpus_model, preprocess_data_kpi, load_lda_model, calculate_coherence, compute_perplexity
import nltk 
import duckdb
import secrets
from typing import Annotated
import mysql.connector
import api_modules
import datetime
import simplejson

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



class database(BaseModel):
    file_name: str = 'test_file'
    file_content: str = 'Mattia è un bimbo di 5 anni che passa tutte le sue giornate a disegnare. In realtà Mattia non si impegna più del necessario per tratteggiare le linee, fare bene le forme o rendere somiglianti le persone che disegna. Mattia ama soprattutto colorare, e ad ogni persona o cosa che disegna associa dei colori specifici. Ogni qual volta disegna suo papà Giuseppe, ad esempio, usa sempre gli stessi colori: i capelli li fa in nero, la maglia è azzurra e i pantaloni rigorosamente rossi. Il papà di Mattia non si veste ovviamente con colori così sgargianti, ma a Mattia piace immaginarlo così.'
    date: str = '2001-05-03'
    publication_name: str = 'test'
    publication_ref: str = 'test'
   

class read_db(BaseModel):
    file_name: str = 'test_file'
 


@app.get('/')
def Say_hello():
    """Vérifie que l'API fonctionne"""
         
    return "Hello, I'm working"



@app.put('/doc/update_model_metrics/{n}/')
def metrics_new_texts(n: Annotated[int, Path(description="Enter number of texts.")],username: Annotated[str, Depends(get_current_username)]):
    query = text(f"select * from new_text LIMIT {n}")
    with engine.connect() as conn:
        result = conn.execute(query)
    lis=[]
    for row in result:
        lis.append(row[5])
    
    lda_model = api_modules.load_lda_model('lda_model')

    id2word = api_modules.load_lda_model('lda_model.id2word')

    topics, perplexity, coherence, alert = api_modules.compute_metrics(lis,lda_model,id2word,threshold_coherence=0.38,threshold_perplexity=-10)

    now = str(datetime.datetime.now())

    cursor = connection.cursor()
    query2 = f"""INSERT INTO metrics (timestamp,coherence,perplexity) VALUES ('{now}','{coherence}','{perplexity}')"""
    cursor.execute(query2)
    connection.commit()
    cursor.close()

    dic = { 'topics': topics,
           'perplexity': perplexity,
           'coherence': coherence,
           'alert': alert}
    return dic

@app.post('/get_metrics')
def get_metrics_from_publication(username: Annotated[str, Depends(get_current_username)]):
    query = text(f"SELECT * FROM metrics ")
    with engine.connect() as conn:
        result = conn.execute(query)
    lis=[]
    for row in result:
        lis.append(row)
       
    test = ['timestamp','coherence','perplexity']
    
    return {test[i] : lis[j][i]  for j in range(len(lis)) for i in range(len(test)) }

@app.get('/doc/retrain_model/{nr_topic_min}/{nr_topic_max}/{n}')
def retrain_model(nr_topic_min: Annotated[int, Path(description="Enter min number of topics.")],nr_topic_max: Annotated[int, Path(description="Enter max number of topics.")],n: Annotated[int, Path(description="Enter number of texts.")], username: Annotated[str, Depends(get_current_username)]):
    
    query = text(f"select * from sources LIMIT {n}")
    with engine.connect() as conn:
        result = conn.execute(query)
    lis=[]

    for row in result:
        lis.append(row[5])
    
    res_df = api_modules.retrain_model(lis, [nr_topic_min,nr_topic_max])

    return res_df.to_dict(orient="records")


@app.put('/get_topic_from_new_text')
def add_data_and_get_topic(database:database,username: Annotated[str, Depends(get_current_username)]):
    cursor = connection.cursor()
    query2 = f"""INSERT INTO new_text (file_name,file_content,date,publication_name,publication_ref) VALUES ('{database.file_name}','{database.file_content}','{database.date}','{database.publication_name}','{database.publication_ref}')"""
    cursor.execute(query2)
    connection.commit()
    cursor.close()
    
    
  
    query = text(f"SELECT * FROM new_text WHERE file_name = '{database.file_name}'")
    corpus_df = pd.read_sql_query(query, engine) 
    
    print(corpus_df['file_content'])

    lda_model = api_modules.load_lda_model('lda_model')

    id2word = api_modules.load_lda_model('lda_model.id2word')

    topics, perplexity, coherence, alert = api_modules.compute_metrics(list(corpus_df['file_content']),lda_model,id2word,threshold_coherence=0.38,threshold_perplexity=-10)
    coherence = simplejson.dumps(coherence, ignore_nan=True)
    if coherence == 'null':
        coherence = 0    
    cursor = connection.cursor()
    query2 = f"""INSERT INTO metrics (timestamp,coherence,perplexity) VALUES ("timestamp",'{coherence}','{perplexity}')"""
    cursor.execute(query2)
    connection.commit()
    cursor.close()

    return {'topics':topics,'coherence':coherence,'perplexity':perplexity}