import mysql.connector
import os
import re
from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password"
)

corpus_url = 'https://zenodo.org/record/4596345/files/ChroniclItaly_3.0_original.zip'


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


def corpus_to_db(zipped_corpus):
    
    """
    Adds records to database from zenodo zipped files.

    Args:
        zipped_corpus (str): Url to zipped corpus.

    Returns:
        list: List of potential errors if any.
    """

    error_logs = []
    unzipped_string = ''
    file_name = ''
    
    try:
        cur = mydb.cursor()
        cur.execute("USE DB")
        
        zipfile = ZipFile(StringIO(zipped_corpus))
        
        for name in zipfile.namelist():
            if '.DS_Store' not in name:
                file_name = name
                file_content = read_txt_content(name)
                file_date = get_date(name)
                file_ref = get_ref(name)

                sql_stmt = f"INSERT INTO Journals(FileName, TextContent, TextDate, PubRef) VALUES('{file_name}', '{file_content}', '{file_date}, '{file_ref}')"

                cur.execute(sql_stmt)

                mydb.commit()
        cur.close()
        mydb.close()

    
    except Exception as e:
        error_logs.append(e)
    
    return error_logs
    


        





# data_file = 'orders.csv'
# with open(data_file, "r") as f:
#     csv_reader = csv.DictReader(f)
#     records = list(csv_reader)

# for record in records:
#     print(record)
#     order_time = record['order_time']
#     date_obj = datetime.strptime(order_time, '%Y-%m-%d %H:%M:%S.%f')
#     item = record['item']
#     sql_stmt = f"INSERT INTO Orders(OrderTime, Item) VALUES('{date_obj}', '{item}')"
#     cur.execute(sql_stmt)
#     mydb.commit()
# cur.close()
# mydb.close()


sql_stmt = f"SELECT * FROM Journals"
cur.execute(sql_stmt)
response = cur.fetchall()
for row in response[:10]:
    print(row[0], row[1])
cur.close()
mydb.close()

