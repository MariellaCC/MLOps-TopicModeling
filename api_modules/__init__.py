import pandas as pd
import nltk
from nltk.corpus import stopwords
import gensim
from gensim.models.phrases import Phrases, Phraser
from gensim import corpora
from gensim.models import LdaModel 
from gensim.models.coherencemodel import CoherenceModel
from gensim.test.utils import datapath
from ast import literal_eval
import datetime
nltk.download('punkt')
nltk.download('stopwords')

def tokenize_documents(dataframe, column_name):
    """
    Tokenize the documents in a DataFrame column.

    Args:
        dataframe (pandas.DataFrame): The DataFrame containing the documents.
        column_name (str): The name of the column containing the documents.

    Returns:
        pandas.DataFrame: The DataFrame with an additional 'tokens' column.
    """
    dataframe['tokens'] = dataframe[column_name].apply(nltk.word_tokenize)
    return dataframe

def preprocess_tokens(dataframe, column_name):
    """
    Preprocess the tokens in a DataFrame column by removing non-alphabetic words and converting them to lowercase.

    Args:
        dataframe (pandas.DataFrame): The DataFrame containing the tokens.
        column_name (str): The name of the column containing the tokens.

    Returns:
        pandas.DataFrame: The DataFrame with an additional 'doc_prep' column.
    """
    dataframe['doc_prep'] = dataframe[column_name].apply(lambda x: [w.lower() for w in x if w.isalpha() and len(w) > 2])
    return dataframe

def load_stopwords(filename):
    """
    Load stopwords from a CSV file.

    Args:
        filename (str): The name of the CSV file.

    Returns:
        list: The stopwords as a list of strings.
    """

    stopwords_df = pd.read_csv(filename)
    cust_stopwords = stopwords_df['stopword'].values.tolist()
    ital_stopwords = stopwords.words('italian')
    en_stopwords = stopwords.words('english')
    cust_stopwords.extend(en_stopwords)
    cust_stopwords.extend(ital_stopwords)

    return cust_stopwords

def remove_stopwords(dataframe, column_name, stopwords):
    """
    Remove stopwords from the tokens in a DataFrame column.

    Args:
        dataframe (pandas.DataFrame): The DataFrame containing the tokens.
        column_name (str): The name of the column containing the tokens.
        stopwords (list): The list of stopwords to remove.

    Returns:
        pandas.DataFrame: The DataFrame with an additional 'doc_prep_nostop' column.
    """
    dataframe['doc_prep_nostop'] = dataframe[column_name].apply(lambda x: [w for w in x if w not in stopwords])
    return dataframe

def create_bigrams(dataframe, column_name, threshold=20, min_count=3):
    """
    Create bigrams from the tokens in a DataFrame column.

    Args:
        dataframe (pandas.DataFrame): The DataFrame containing the tokens.
        column_name (str): The name of the column containing the tokens.
        threshold (int): Represents a threshold for forming the phrases (default: 20).
        min_count (int): Represents the minimum count of the phrases (default: 3).

    Returns:
        pandas.DataFrame: The DataFrame with an additional 'bigrams' column.
    """
    bigram = Phrases(dataframe[column_name], min_count=min_count, threshold=threshold)
    bigram_mod = Phraser(bigram)
    dataframe['bigrams'] = [bigram_mod[doc] for doc in dataframe[column_name]]
    return dataframe

def get_id2word(bigrams):
    """
    Get id2word Dictionary for the corpus.

    Args:
        bigrams (pandas.Series): The corpus data containing bigrams.

    Returns:
        gensim.corpora.Dictionary: The dictionary mapping of words to IDs.

    """
    id2word = corpora.Dictionary(bigrams)
    id2word.filter_extremes(no_below=5)

    return id2word

def get_bow(id2word,bigrams):
    """
    Get bag of words for a given dictionary.

    Args:
        gensim.corpora.Dictionary: The dictionary mapping of words to IDs.
        bigrams (pandas.Series): The corpus data containing bigrams.

    Returns:
        list: The preprocessed corpus as a list of bag-of-words.

    """
    corpus = [id2word.doc2bow(text) for text in bigrams]
    return corpus

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

def compute_coherence(lda_model, bigrams, corpus, id2word):
    """
    Compute coherence value for the given LDA model.

    Args:
        lda_model (gensim.models.LdaModel): The LDA model.
        bigrams (list): Preprocessed data (bigrams).
        corpus (list): The corpus in Bow format.
        id2word (gensim.corpora.Dictionary): The id2word dictionary.

    Returns:
        float: The coherence value.
    """
    coherencemodel = CoherenceModel(model=lda_model, texts=bigrams, corpus=corpus, dictionary=id2word, coherence='c_v')
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

def get_topics(lda_model):
    """
    Retrieves topics for an LDA model.

    Args:
        lda_model (gensim.models.LdaModel): The LDA model.

    Returns:
        list: The topics.
    """

    topics = lda_model.get_topics

    return topics






def compute_metrics(texts,lda_model,id2word,threshold_coherence=0.38,threshold_perplexity=-10):
    """
    Compute metrics, raise alert and insert texts in train table if threshold is reached.

    Args:
        nr_texts (int): Number of texts to send to pre-trained model.
        ldamodel (gensim.LdaModel): pre-trained model.

    Returns:
        alert (str): Alert if the corpus needs to be retrained.

    """

    # Create df from new texts
    new_texts = pd.DataFrame(texts,columns=['file_content'])

    # Tokenize documents
    corpus_df = tokenize_documents(new_texts, 'file_content')

    # Preprocess tokens
    corpus_df = preprocess_tokens(corpus_df, 'tokens')

    # Load stopwords
    stopwords_list = load_stopwords('stop_words.csv')

    # Remove stopwords
    corpus_df = remove_stopwords(corpus_df, 'doc_prep', stopwords_list)

    # Create bigrams
    corpus_df = create_bigrams(corpus_df, 'doc_prep_nostop')

    corpus = get_bow(id2word,corpus_df['bigrams'])

    # add the new texts to the model to check the metrics and see if a threshold is triggered, in case it is the model will need to be retrained
    lda_model.update(corpus)

    coherence = compute_coherence(lda_model, corpus_df['bigrams'], corpus, id2word)

    perplexity = compute_perplexity(lda_model, corpus)

    alert = "Retrain needed" if (coherence < threshold_coherence or perplexity > threshold_perplexity) else None

    return lda_model.print_topics(num_words=10), perplexity, coherence, alert


def retrain_model(texts, topic_nr):
    """
    Retrain model and compute metrics for range of topic numbers.

    Args:
        texts (list): List containing the texts to train the model.
        topic_nr (list): List containing min and max number of topics to test.

    Returns:
        error (str): Error message.

    """

    # Create df from new texts
    corpus_df = pd.DataFrame(texts,columns=['file_content'])

    # Tokenize documents
    corpus_df = tokenize_documents(corpus_df, 'file_content')

    # Preprocess tokens
    corpus_df = preprocess_tokens(corpus_df, 'tokens')

    # Load stopwords
    stopwords_list = load_stopwords('stop_words.csv')

    # Remove stopwords
    corpus_df = remove_stopwords(corpus_df, 'doc_prep', stopwords_list)

    # Create bigrams
    corpus_df = create_bigrams(corpus_df, 'doc_prep_nostop')

    id2word = get_id2word(corpus_df['bigrams'])

    corpus = get_bow(id2word,corpus_df['bigrams'])

    topics_nr = []
    coherence_values_gensim = []
    perplexitys = []
    models = []
    models_idx = [x for x in range(topic_nr[0],topic_nr[1])]
    for num_topics in range(topic_nr[0],topic_nr[1]):
        model = LdaModel(corpus, id2word=id2word, num_topics=num_topics, eval_every = None, chunksize=100,
                                          passes=10,random_state=100)
        models.append(model)
        coherencemodel = CoherenceModel(model=model, texts=corpus_df, dictionary=id2word, coherence='c_v')
        coherence_value = coherencemodel.get_coherence()
        perplexity = model.log_perplexity(corpus)
        perplexitys.append(perplexity)
        coherence_values_gensim.append(coherence_value)
        topics_nr.append(str(num_topics))

    df_coherence = pd.DataFrame(topics_nr, columns=['Number of topics'])
    df_coherence['Coherence'] = coherence_values_gensim
    df_coherence['Perplexity'] = perplexitys

    return df_coherence