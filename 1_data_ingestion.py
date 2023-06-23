# dataset can be obtained via https://zenodo.org/record/4596345#.Yk2flG5Bz0o
# folder containing one or more sub-folders 
# sub-folders are publications
# within each sub-folder, collection of text files that each constitute a document
# for now, supported naming pattern for text files is as such: '/sn86069873/1900-01-05/'
# LCCN title information and publication date (yyyy-mm-dd)
# users will need to provide publication names that match title information, or to use the metadata file


"""
The code performs the following steps:

1. The preprocess_data function takes the folder name, publication references, publication names, start date, and end date as inputs. It processes the data by extracting information from files and performing filtering.
2. The get_files_list function returns a flattened list of file paths in the specified folder, excluding '.DS_Store' files.
3. The get_ref function extracts the publication reference from a file name.
4. The get_date function extracts the date from a file name.
5. The read_txt_content function reads and returns the content of a text file.
6. In the preprocess_data function, the folder path is obtained using os.path.abspath based on the provided folder name.
7. The file paths are obtained by calling get_files_list and stored in a DataFrame called sources.
8. Additional columns are added to the sources DataFrame, including 'date', 'publication_ref', and 'publication_name'. The 'date' column is obtained by calling get_date, the 'publication_ref' column is obtained by calling get_ref, and the 'publication_name' column is generated by replacing the publication references using the provided pub_refs and pub_names dictionaries.
9. A connection to DuckDB is established using duckdb.connect.
10. The sources DataFrame is registered as a DuckDB table called 'sources'.
11. A SQL query is constructed based on the provided start and end dates.
12. The query is executed using conn.execute and the result is fetched as a DataFrame called subset_df.
13. The 'file_name' column in subset_df is modified to have a forward slash as the path separator and remove any backslashes using a lambda function.
14. The 'file_content' column is generated by reading the text content of the files using read_txt_content.
15. Additional columns 'chars_count' and 'words_count' are added to subset_df, representing the character count and word count of the file content, respectively.
16. The subset_df DataFrame, containing the preprocessed data, is returned from the preprocess_data function.
17. Finally, the subset_df DataFrame is saved to a CSV file named 'subset.csv' using the to_csv method.

"""
import os
import re
import pandas as pd
import duckdb

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

# indicate name of the folder containing data, for example 'data_tm_workflow'
folder_name = 'CI_newspaper_subcorpora'
pub_refs = ["2012271201", "sn85054967", "sn93053873", "sn85066408", "sn85055164", "sn84037024", "sn84037025", "sn84020351", "sn86092310", "sn92051386"]
pub_names = ["Cronaca_Sovversiva", "Il_Patriota", "L'Indipendente", "L'Italia", "La_Libera_Parola", "La_Ragione", "La_Rassegna", "La_Sentinella", "La_Sentinella_del_West", "La_Tribuna_del_Connecticut"]
date_ref_1 = "1903-06-06"
date_ref_2 = "1919-05-01"

# Preprocess the data and obtain the subset dataframe
subset_df = preprocess_data(folder_name, pub_refs, pub_names, date_ref_1, date_ref_2)

# Save the subset dataframe to a CSV file
subset_df.to_csv('subset.csv')