import uvicorn 
import gensim
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
from nltk.corpus import stopwords
from fastapi import FastAPI
from fastapi import Header
from pydantic import BaseModel
import pandas as pd 
import numpy as np 
from gensim.test.utils import datapath
from ast import literal_eval
from gensim import corpora
import os
import re 
from data_ingestion import read_txt_content, get_date, get_ref, get_files_list
from pre_processing import load_data,tokenize_documents, preprocess_tokens, load_stopwords, remove_stopwords, create_bigrams, save_dataframe
from kpi import load_corpus_model, preprocess_data_kpi, load_lda_model, calculate_coherence
import nltk 
import duckdb

nltk.download('punkt')
nltk.download('stopwords')

app = FastAPI()

folder_name = 'CI_newspaper_subcorpora'
pub_refs = ["2012271201", "sn85054967", "sn93053873", "sn85066408", "sn85055164", "sn84037024", "sn84037025", "sn84020351", "sn86092310", "sn92051386"]
pub_names = ["Cronaca_Sovversiva", "Il_Patriota", "L'Indipendente", "L'Italia", "La_Libera_Parola", "La_Ragione", "La_Rassegna", "La_Sentinella", "La_Sentinella_del_West", "La_Tribuna_del_Connecticut"]


def preprocess_data(folder_name, pub_refs, pub_names, date_ref_1, date_ref_2):
    """
    Preprocesses the data by extracting information from files and performing filtering.

    Args:
        folder_name (str): Name of the folder containing the files.
        pub_refs (dict): Dictionary mapping publication references.
        pub_names (dict): Dictionary mapping publication names.
        date_ref_1 (str): Start date for filtering.
        date_ref_2 (str): End date for filtering.

    Returns:
        pandas.DataFrame: Preprocessed data subset.
    """
    folder_path = os.path.abspath(folder_name)
    files_list_flat = get_files_list(folder_path)

    sources = pd.DataFrame(files_list_flat, columns=['file_name'])
    sources['date'] = sources['file_name'].apply(get_date)
    sources['publication_ref'] = sources['file_name'].apply(get_ref)
    sources["date"] = pd.to_datetime(sources["date"])
    sources['publication_name'] = sources['publication_ref'].replace(pub_refs, pub_names)

    # Establish connection to DuckDB
    conn = duckdb.connect(database=':memory:')

    # Create DuckDB table
    conn.register('sources', sources)

    query = f"SELECT * FROM sources WHERE date <= DATE '{date_ref_2}' AND date > DATE '{date_ref_1}'"

    # Execute the query and fetch the result as a DataFrame
    subset_df = conn.execute(query).fetchdf()

    subset_df['file_name'] = subset_df['file_name'].apply(lambda x: '/' + x.replace("\\", "/"))  

    subset_df['file_content'] = subset_df['file_name'].apply(lambda x: read_txt_content(os.path.join(folder_path, x.lstrip('/'))))
    subset_df['chars_count'] = subset_df['file_content'].apply(len)
    subset_df['words_count'] = subset_df['file_content'].apply(lambda x: len(x.split()))

    return subset_df

class topic(BaseModel):
    num_topic: int = 10
    date_ref_1 :str = "1903-06-06"
    date_ref_2 : str = "1919-05-01"

class database(BaseModel):
    pub_refs: str 
    pub_names: str 

@app.get('/')
def Say_hello():
    """Vérifie que l'API fonctionne"""
         
    return "Hello, I'm working"

@app.post('/topic')
def get_topic(topic:topic):
    #data ingestion
    
    subset_df = preprocess_data(folder_name, pub_refs, pub_names, topic.date_ref_1, topic.date_ref_2)
    subset_df.to_csv('subset.csv')

    #pre process
    corpus_df = load_data('subset.csv')
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

    topic_print_model = lda.print_topics(num_words=topic.num_topic)
    coherence_value = calculate_coherence(lda, bigrams, corpus, id2word)
    dic = { topic_print_model[i][0] : topic_print_model[i][1]  for i in range (7)}
    
    return {'topic':dic, 'coherence':coherence_value}

@app.put('/database')
def add_data(new:database):

    """ l'idée est de rajouter un fichier directement dans la base de donnée"""
   
    return {'test':'hi'}

