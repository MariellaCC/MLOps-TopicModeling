"""
1. The code defines several functions to perform specific tasks:
• load_corpus_model(file_path): This function loads the corpus model from a CSV file, where each row contains preprocessed data in the form of bigrams. It returns the preprocessed data as a list of bigrams.
• preprocess_data(bigrams): This function preprocesses the data by creating an id2word dictionary and a corpus. It takes the list of bigrams as input and returns the created id2word dictionary and the corpus.
• load_lda_model(model_path): This function loads an LDA model from disk. It takes the path to the LDA model file as input and returns the loaded LDA model.
• calculate_coherence(lda_model, bigrams, corpus, id2word): This function calculates the coherence value for the given LDA model. It takes the LDA model, the list of bigrams, the corpus, and the id2word dictionary as input and returns the coherence value.
2. File paths are defined for the corpus model file (corpus_model_file) and the LDA model file (lda_model_file).
3. The code begins the execution by calling the load_corpus_model() function and passing the corpus_model_file path. This loads the corpus model from the CSV file and returns the preprocessed data (bigrams).
4. The preprocess_data() function is called, passing the bigrams obtained from the previous step. This function creates the id2word dictionary and the corpus based on the bigrams. It returns the created id2word dictionary and the corpus.
5. The load_lda_model() function is called, passing the lda_model_file path. This function loads the LDA model from the specified file and returns the loaded LDA model.
6. The calculate_coherence() function is called, passing the loaded LDA model, the bigrams, the corpus, and the id2word dictionary. This function calculates the coherence value using the provided parameters.
7. Finally, the coherence value is printed to the console using print(coherence_value).
The code's execution flow ensures that the corpus model is loaded, preprocessed, and used in combination with the LDA model to calculate the coherence value.
"""

import pandas as pd
import gensim
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.hdpmodel import HdpModel

from gensim.test.utils import datapath
from ast import literal_eval
from gensim import corpora
import os

def load_corpus_model(file_path):
    """
    Load the corpus model from a CSV file and return the preprocessed data.

    Args:
        file_path (str): Path to the CSV file containing the corpus model.

    Returns:
        list: Preprocessed data (bigrams).
    """
    corpus_model = pd.read_csv(file_path)
    bigrams = corpus_model['bigrams'].apply(literal_eval)
    return bigrams

def preprocess_data_kpi(bigrams):
    """
    Preprocess the data by creating the id2word dictionary and the corpus.

    Args:
        bigrams (list): Preprocessed data (bigrams).

    Returns:
        gensim.corpora.Dictionary: The id2word dictionary.
        list: The corpus.
    """
    id2word = corpora.Dictionary(bigrams)
    id2word.filter_extremes(no_below=5)
    corpus = [id2word.doc2bow(text) for text in bigrams]
    return id2word, corpus

def load_lda_model(model_path):
    """
    Load the LDA model from disk.

    Args:
        model_path (str): Path to the LDA model file.

    Returns:
        gensim.models.LdaModel: The loaded LDA model.
    """
    lda = LdaModel.load(model_path)
    return lda

def calculate_coherence(lda_model, bigrams, corpus, id2word):
    """
    Calculate coherence value for the given LDA model.

    Args:
        lda_model (gensim.models.LdaModel): The LDA model.
        bigrams (list): Preprocessed data (bigrams).
        corpus (list): The corpus.
        id2word (gensim.corpora.Dictionary): The id2word dictionary.

    Returns:
        float: The coherence value.
    """
    coherencemodel = CoherenceModel(model=lda_model, texts=bigrams, corpus=corpus, dictionary=id2word, coherence='u_mass')
    coherence_value = coherencemodel.get_coherence()
    return coherence_value

def compute_perplexity(lda_model, corpus):
    """
    Computes perplexity value for the given LDA model.

    Args:
        lda_model (gensim.models.LdaModel): The LDA model.
        corpus (list): The corpus.

    Returns:
        float: The perplexity value.
    """
    
    perplexity = lda_model.log_perplexity(corpus)
    return perplexity

if __name__ == "__main__":
# File paths
    corpus_model_file = 'corpus_model.csv'

#Generic directory with the data and the saved model. Will have to readapt if using a DB system
    current_directory = os.getcwd()
    lda_model_file = os.path.join(current_directory, 'lda_model')  # Construct the path to the LDA model file

# Load corpus model
    bigrams = load_corpus_model(corpus_model_file)

# Preprocess data
    id2word, corpus = preprocess_data_kpi(bigrams)

# Load LDA model
    lda = load_lda_model(lda_model_file)

# Calculate coherence
    coherence_value = calculate_coherence(lda, bigrams, corpus, id2word)

# Print coherence value
    print(coherence_value)

    perplexity_score = compute_perplexity(lda, corpus)

    print(perplexity_score)
