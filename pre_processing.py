# link to custom stop words: https://drive.google.com/file/d/1VVfW6AKPbb7_fICOG73lEgkXmmZ6BkpC/view?usp=sharing
# Upload stop words list into Colab files before proceeding with the next cells

""""

Loads the data from the 'subset.csv' file into the 'corpus_df' DataFrame.
Tokenizes the documents in the 'file_content' column and adds the 'tokens' column to the DataFrame.
Preprocesses the tokens in the 'tokens' column by removing non-alphabetic words and converting them to lowercase, and adds the 'doc_prep' column to the DataFrame.
Loads stopwords from the 'stop_words.csv' file.

1. Loads the data from the 'subset.csv' file into the 'corpus_df' DataFrame.
2. Tokenizes the documents in the 'file_content' column and adds the 'tokens' column to the DataFrame.
3. Preprocesses the tokens in the 'tokens' column by removing non-alphabetic words and converting them to lowercase, and adds the 'doc_prep' column to the DataFrame.
4. Loads stopwords from the 'stop_words.csv' file.
5. Removes stopwords from the tokens in the 'doc_prep' column using the provided list of stopwords, and adds the 'doc_prep_nostop' column to the DataFrame.
6. Creates bigrams from the tokens in the 'doc_prep_nostop' column using the provided threshold and minimum count. The resulting bigrams are stored in the 'bigrams' column of the DataFrame.
7. Saves the processed data from the 'bigrams' column of the DataFrame to the 'corpus_model.csv' file using the save_dataframe function.
Overall, the code loads data from a CSV file, tokenizes the text documents, performs preprocessing on the tokens by removing non-alphabetic words and converting them to lowercase, removes stopwords, creates bigrams from the preprocessed tokens, and saves the processed data to a new CSV file.

"""

import pandas as pd
import nltk
from nltk.corpus import stopwords
import gensim
from gensim.models.phrases import Phrases, Phraser

nltk.download('punkt')
nltk.download('stopwords')

def load_data(filename):
    """
    Load data from a CSV file into a pandas DataFrame.
    
    Args:
        filename (str): The name of the CSV file.
    
    Returns:
        pandas.DataFrame: The loaded DataFrame.
    """
    return pd.read_csv(filename)

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
    
    #ital_stopwords = stopwords.words('italian')
    #en_stopwords = stopwords.words('english')
    stopwords_df = pd.read_csv(filename)
    #stopwords_df.concat(en_stopwords)
    #stopwords_df.concat(ital_stopwords)
    return stopwords_df['stopword'].values.tolist()

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

def save_dataframe(dataframe, filename):
    """
    Save a DataFrame to a CSV file.
    
    Args:
        dataframe (pandas.DataFrame): The DataFrame to save.
        filename (str): The name of the CSV file.
    """
    dataframe.to_csv(filename, index=False)

if __name__ == "__main__":
# Load data
    corpus_df = load_data('subset.csv')

# Tokenize documents
    corpus_df = tokenize_documents(corpus_df, 'file_content')

# Preprocess tokens
    corpus_df = preprocess_tokens(corpus_df, 'tokens')

# Load stopwords
    stopwords = load_stopwords('stop_words.csv')

# Remove stopwords
    corpus_df = remove_stopwords(corpus_df, 'doc_prep', stopwords)

# Create bigrams
    corpus_df = create_bigrams(corpus_df, 'doc_prep_nostop')

# Save processed data
    save_dataframe(corpus_df['bigrams'], 'corpus_model.csv')