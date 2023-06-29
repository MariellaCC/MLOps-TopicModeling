import os
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from gensim.models.phrases import Phrases, Phraser
from pre_processing import load_data, tokenize_documents, preprocess_tokens, load_stopwords


# Set the current directory
current_directory = os.getcwd()

# Test load_data function
def test_load_data():
    filename = os.path.join(current_directory, 'subset.csv')
    corpus_df = load_data(filename)
    assert isinstance(corpus_df, pd.DataFrame), "load_data should return a pandas DataFrame"
    assert not corpus_df.empty, "Loaded DataFrame should not be empty"
    assert "file_content" in corpus_df.columns, "Loaded DataFrame should have a 'file_content' column"
    print("test_load_data passed successfully!")


# Test load_stopwords function
def test_load_stopwords():
    filename = os.path.join(current_directory, 'stop_words.csv')
    stopwords_list = load_stopwords(filename)
    assert isinstance(stopwords_list, list), "load_stopwords should return a list"
    assert len(stopwords_list) > 0, "Loaded stopwords list should not be empty"
    print("test_load_stopwords passed successfully!")

    
test_load_data()
test_load_stopwords()