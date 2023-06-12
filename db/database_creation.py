import os
import re
import pandas as pd
from sqlalchemy import URL, create_engine


url_object = URL.create(
    "mysql+pymysql",
    username="root",
    password="password",
    host="localhost",
    database="DB",
)

engine = create_engine(url_object)

folder_name = 'CI_newspaper_subcorpora'
pub_refs = ["2012271201", "sn85054967", "sn93053873", "sn85066408", "sn85055164", "sn84037024", "sn84037025", "sn84020351", "sn86092310", "sn92051386"]
pub_names = ["Cronaca_Sovversiva", "Il_Patriota", "L'Indipendente", "L'Italia", "La_Libera_Parola", "La_Ragione", "La_Rassegna", "La_Sentinella", "La_Sentinella_del_West", "La_Tribuna_del_Connecticut"]



def get_files_list(folder_path):
    """
    Returns a flattened list of file paths in the specified folder, excluding '.DS_Store' files.

    Args:
        folder_path (str): Path to the folder containing the files.

    Returns:
        list: A list of file paths.
    """
    publications_list = os.listdir(folder_path)
    publications_list = [file for file in publications_list if '.DS_Store' not in file]

    files_list = []
    for pub in publications_list:
        files = os.listdir(os.path.join(folder_path, pub))
        files = [os.path.join(pub, file) for file in files]
        files_list.append(files)

    files_list_flat = [item for sublist in files_list for item in sublist]
    return files_list_flat

def get_ref(file):
    """
    Extracts the publication reference from a file name.

    Args:
        file (str): File name.

    Returns:
        str: Publication reference.
    """
    ref_match = re.findall(r'(\w+\d+)_\d{4}-\d{2}-\d{2}_', file)
    return ref_match[0]

def get_date(file):
    """
    Extracts the date from a file name.

    Args:
        file (str): File name.

    Returns:
        str: Date in the format 'YYYY-MM-DD'.
    """
    date_match = re.findall(r'_(\d{4}-\d{2}-\d{2})_', file)
    return date_match[0]

def read_txt_content(file_path):
    """
    Reads and returns the content of a text file.

    Args:
        file_path (str): Path to the text file.

    Returns:
        str: Content of the text file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return ' ' + file.read().replace('\n', ' ') + ' '



def create_dataset(folder_name, pub_refs, pub_names):
    """
    Preprocesses the data by extracting information from files and performing filtering.

    Args:
        folder_name (str): Name of the folder containing the files.
        pub_refs (dict): Dictionary mapping publication references.
        pub_names (dict): Dictionary mapping publication names.

    Returns:
        pandas.DataFrame: Preprocessed data subset.
    """
    folder_path = os.path.abspath(folder_name)
    files_list_flat = get_files_list(folder_path)

    sources = pd.DataFrame(files_list_flat, columns=['file_name'])
    sources['date'] = sources['file_name'].apply(get_date)
    sources['publication_ref'] = sources['file_name'].apply(get_ref)
    sources['publication_name'] = sources['publication_ref'].replace(pub_refs, pub_names)
    # sources['file_name'] = sources['file_name'].apply(lambda x: '/' + x.replace("\\", "/"))  
    sources['file_content'] = sources['file_name'].apply(lambda x: read_txt_content(os.path.join(folder_path, x.lstrip('/'))))

    return sources



def corpus_to_db(sources_df):
    
    """
    Adds records to database from zenodo zipped files.

    Args:
        path (str): Local path to corpus folder.

    Returns:
        list: List of potential errors if any.
    """

    error_logs = []
    
    try:

        sources_df.to_sql('Journals', con=engine, if_exists='replace')

    
    except Exception as e:
        print(e)
        error_logs.append(e)
    
    return error_logs


sources_df = create_dataset(folder_name, pub_refs, pub_names)
corpus_to_db(sources_df)