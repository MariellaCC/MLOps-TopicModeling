import pandas as pd
import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.test.utils import datapath
from ast import literal_eval
import os

"""

1. The code defines several functions to modularize the code and improve reusability. These functions are:
• load_corpus_model: Loads the corpus model from a CSV file and returns the bigrams data as a Pandas Series.
• preprocess_corpus: Preprocesses the corpus by creating a dictionary mapping of words to IDs and converting the bigrams data into a list of bag-of-words.
• train_lda_model: Trains an LDA model on the preprocessed corpus using the Gensim library and returns the trained model.
• save_model: Saves the trained LDA model to a file.
2. The file paths are defined for the input corpus model CSV file (corpus_model_file) and the output LDA model file (model_output_file).
3. The code calls the load_corpus_model function, passing the corpus_model_file path, to load the corpus model from the CSV file. The bigrams data is extracted from the loaded DataFrame using literal_eval to convert the string representation back into a list.
4. The code calls the preprocess_corpus function, passing the bigrams data, to preprocess the corpus. It creates a dictionary (id2word) mapping words to IDs and converts the bigrams data into a list of bag-of-words (corpus).
5. The code calls the train_lda_model function, passing the preprocessed corpus and id2word dictionary. It trains an LDA model using the Gensim library, specifying the number of topics (num_topics) and the random state for reproducibility (random_state). The trained model (lda_model) is returned.
6. The code calls the save_model function, passing the lda_model and the model_output_file path. It saves the trained LDA model to the specified file using the Gensim library's save method.
7. The execution of the code completes, and the trained LDA model is saved to the specified output file.
By following this step-by-step execution, the code loads the corpus model data, preprocesses the corpus, trains an LDA model on the preprocessed corpus, and saves the trained model to a file.

"""



def load_corpus_model(file_path):
    """
    Load the corpus model from a CSV file.

    Args:
        file_path (str): The path to the corpus model CSV file.

    Returns:
        pandas.Series: The corpus model data.

    """
    corpus_model = pd.read_csv(file_path)
    bigrams = corpus_model['bigrams'].apply(literal_eval)
    return bigrams


def preprocess_corpus(bigrams):
    """
    Preprocess the corpus for LDA training.

    Args:
        bigrams (pandas.Series): The corpus data containing bigrams.

    Returns:
        gensim.corpora.Dictionary: The dictionary mapping of words to IDs.
        list: The preprocessed corpus as a list of bag-of-words.

    """
    id2word = corpora.Dictionary(bigrams)
    id2word.filter_extremes(no_below=5)
    corpus = [id2word.doc2bow(text) for text in bigrams]
    return id2word, corpus


def train_lda_model(corpus, id2word, num_topics=7, random_state=100):
    """
    Train an LDA model on the given corpus.

    Args:
        corpus (list): The preprocessed corpus as a list of bag-of-words.
        id2word (gensim.corpora.Dictionary): The dictionary mapping of words to IDs.
        num_topics (int): The number of topics to generate (default: 7).
        random_state (int): The random state for reproducibility (default: 100).

    Returns:
        gensim.models.LdaModel: The trained LDA model.

    """
    model = LdaModel(corpus, id2word=id2word, num_topics=num_topics, random_state=random_state, eval_every=None)
    return model


def save_model(model, output_path):
    """
    Save the trained LDA model to a file.

    Args:
        model (gensim.models.LdaModel): The trained LDA model.
        output_path (str): The path to save the model.

    """
    model.save(output_path)


if __name__ == "__main__":
# Define the file paths
    corpus_model_file = 'corpus_model.csv'
    model_output_file = os.path.join(os.getcwd(), 'lda_model')

# Load the corpus model
    corpus_model = load_corpus_model(corpus_model_file)

# Preprocess the corpus
    id2word, corpus = preprocess_corpus(corpus_model)

# Train the LDA model
    lda_model = train_lda_model(corpus, id2word)

# Save the trained model to a file
    save_model(lda_model, model_output_file)

""""

OLD FOR REF prior to confirmation of the output files for the above automation script

import pandas as pd
import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.test.utils import datapath
from ast import literal_eval


corpus_model = pd.read_csv('corpus_model.csv')

# la ligne suivante est nécessaire car la conversion en csv transforme les arrays en string, ce qui est problématique car ensuite le id2word ne marche pas
# on pourra enlever cela quand on passera avec un ystème BDD
# le temps de processing est assez long
bigrams = corpus_model['bigrams'].apply(literal_eval)

#LDA prep

id2word = corpora.Dictionary(bigrams)

id2word.filter_extremes(no_below=5)

corpus = [id2word.doc2bow(text) for text in bigrams]

num_topics = 7

model = LdaModel(corpus, id2word=id2word, num_topics=num_topics, random_state=100, eval_every = None)

#saving model to file

model_file = datapath("/Users/mariellacc/Documents/GitHub/MLOps-TopicModeling/lda_model")

model.save(model_file)
"""