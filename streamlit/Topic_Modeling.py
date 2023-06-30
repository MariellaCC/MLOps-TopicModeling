
import streamlit as st
import pandas as pd 
import requests
from requests.auth import HTTPBasicAuth


#Page configuration 
st.set_page_config(page_title="Topic Modeling",page_icon='🌍',layout="wide", initial_sidebar_state="auto")

#Barre de Navigation 
st.sidebar.title('Navigation')
#Différentes pages du site 
pages = ['Home','Introduction','Database','API','Isolation' , 'Tests', 'Monitoring', 'Conclusion/Outlooks', 'Bonus: Web interface']
page = st.sidebar.radio(' ',pages)

                                                    #Page 1: Introduction 
    
    
    
    
    
    
if page == pages[0]:
#Project Title
    st.markdown("<h1 style='text-align: center; color: red;'>Topic Modeling</h1>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: white;'>DataScientest Project / MLOps FEV23</h2>", unsafe_allow_html=True)
 #Team 
    st.subheader('By Florian, Mariella, Juan')
 #Picture   
 #   st.image('streamlit_app/assets/rechauffement.png', width = 1200)
 #Project description    
    st.write(
        """
        
        The project MLOps - Topic Modeling aims at deploying a topic modeling workflow with an MLOps approach.
As an underlying workflow, we selected the project Topic Modelling with Gensim. \n 
A workflow for the Humanities available under the following repo: https://github.com/DHARPA-Project/TopicModelling- (1). The reference materials that we used were forked into the "reference" directory of the current project.      

        """
    )
if page == pages[1]:
    st.markdown("<h1 style='text-align: center; color: white;'>Introduction</h1>", unsafe_allow_html=True)
    st.write("""
Topic Modeling:\n
As digitally available textual repositories are becoming larger and larger, 
traditional close reading methods are no longer sufficient to analyse mass of digital data.
Topic Modeling is a computational, statistical method to discover patterns and topics in large collections of text.\n 
Data:\n
This open access collection (https://zenodo.org/record/4596345#.Yk2flG5Bz0o ) includes the digitized front pages of 10 Italian language newspapers published in California, Connecticut, Pennsylvania, Vermont, and West Virginia. It totals 8,653 issues and contains 21,454,455 words. The titles are: L’Italia, Cronaca sovversiva, La libera parola, The patriot, La ragione, La rassegna, La sentinella del West Virginia, L’Indipendente, La Sentinella, and and La Tribuna del Connecticut. The material was collected from Chronicling America, an Internet-based, searchable database of U.S. newspapers published in the United States from 1789 to 1963 made available by the Library of Congress. The corpus features mainstream (prominenti), anarchic (sovversivi), and independent newspapers thus providing a very nuanced picture of the Italian immigrant community in the United States at the turn of the twentieth century.\n 
API goal:\n
Our API aims at enabling users to update a pre-trained model that has been trained with the collection described above, and to monitor the evolution of metrics over time.
We have chosen two metrics to do so: coherence and perplexity. The coherence score measures the statistical accuracy of the model, whereas perplexity helps determining whether the model is too specific or too generic for a corpus of text.
If thresholds are reached, the API alerts users and offers a route to retrain the model in order to assess again the number of topics to be used, as a preparation step before creating a new model.

    """)
    

if page == pages[3]:

    st.markdown("<h1 style='text-align: center; color: white;'>API</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; '>API paths</h1>", unsafe_allow_html=True)
    st.write(""" 
    First path: check API 
    
    """)
    st.image('streamlit/streamlit_images/api_1.png', width = 1200)
    st.write(""" 
    Second path : Choose n texts and return topics, lcoherence and perplexity metrics, as well as an alert if metrics are too low
    
    """)
    st.image('streamlit/streamlit_images/api_2.png', width = 1200)
    st.write(""" 
    Third path: return last metrics 
    
    """)
    st.image('streamlit/streamlit_images/api_3.png', width = 1200)
    st.write(""" 
    Foutrh: réentraine le modèle pour un nombre n de textes avec nr_topic_num le minimum de topic voulu et nr_topic_max le nombre maximum voulu et retourne les métriques pour chaque nombre de topics     
    
    """)

    st.image('streamlit/streamlit_images/api_4.png', width = 1200)
    st.write(""" 
    Fifth path: add txt in database and return topics and metrics     
    
    """)
    st.image('streamlit/streamlit_images/api_5.png', width = 1200)
    st.markdown("<h2 style='text-align: center; '>Démo</h1>", unsafe_allow_html=True)
    st.write(""" http://localhost:8000/docs""")

if page == pages[2]:

    st.markdown("<h1 style='text-align: center; color: white;'>Database</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; '>SQL</h1>", unsafe_allow_html=True)
    st.write(""" 
    Databse structure will not change over time.\n
    We need only 3 elements: date, publication, and text\n
    Data are open source and not massive\n
    SQL is enough for this project
   
    """)
    st.write(""" Sources database structure""")
            
    st.image('streamlit/streamlit_images/bdd_sources.png', width = 1200)
    st.write(""" Metrics database structure""")
    col1, col2, col3= st.columns([1,1,1])       
    with col2:                
        st.image('streamlit/streamlit_images/bdd_metrics.png', width = 400)
    


if page == pages[4]:

    st.markdown("<h1 style='text-align: center; color: white;'>Isolation</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; '>Docker</h1>", unsafe_allow_html=True)
    st.write(""" 
    DOckerfile Database creation
    
    """)
    st.code(""" FROM mysql/mysql-server
    ENV MYSQL_DATABASE=DB \
    MYSQL_ROOT_PASSWORD=password \
    MYSQL_ROOT_HOST=%
    ADD ./db/schema.sql /docker-entrypoint-initdb.d
    COPY ./db/database_creation.py /app/database_creation.py
    EXPOSE 3306""", language='sql')

    st.write(""" 
    DOckerfile filling database
    
    """)

    st.code(""" FROM python:3.10-slim
    RUN apt-get update && apt-get install -y python3-pip
    COPY ./requirements.txt /app/requirements.txt
    WORKDIR /app
    RUN pip install -r requirements.txt
    COPY ./db/database_creation.py ./
    COPY ./db/CI_newspaper_subcorpora ./CI_newspaper_subcorpora
    CMD ["python", "database_creation.py"]""", language='sql')

    st.write(""" 
    DOckerfile API
    
    """)

    st.code(""" FROM python:3.10-slim
    RUN apt-get update && apt-get install -y python3-pip
    COPY ./requirements.txt /app/requirements.txt
    WORKDIR /app
    RUN pip install -r requirements.txt
    COPY ./api_modules ./api_modules
    COPY api.py ./
    COPY ./python_code ./python_code
    COPY stop_words.csv subset.csv lda_model lda_model.state lda_model.id2word lda_model.expElogbeta.npy ./
    CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8002"]""", language='sql')

    st.write(""" 
    DOcker-Compose
    
    """)

    st.code(""" version: "3.9"
services:

  tm_db:
    image: mysql:latest
    volumes:
      - ./db:/docker-entrypoint-initdb.d
    environment:
      MYSQL_ROOT_PASSWORD: "password"
      MYSQL_TCP_PORT: 3306
    ports:
      - "3307:3306"
    healthcheck:
      test: ["CMD", "mysqladmin" ,"ping", "-h", "tm_db"]
      interval: 5s
      timeout: 5s
      retries: 5

  fill_bdd:
    depends_on:
      tm_db:
        condition: service_healthy
    build:
      context: .
      dockerfile: dockerfile_fill_bdd

  start_api:
    depends_on:
      fill_bdd:
        condition: service_completed_successfully
    restart: on-failure:15
    build:
      context: .
      dockerfile: dockerfile_api
    ports:
      - "8000:8002" """, language='sql')
    

if page == pages[5]:
    
    st.markdown("<h1 style='text-align: center; color: white;'>Tests</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>GitHub Actions</h1>", unsafe_allow_html=True)
    st.write("https://github.com/MariellaCC/MLOps-TopicModeling/actions")
    st.code("""def test_api_working():
    response = requests.get('http://localhost:8000/')
    assert response.json() == "Hello, I'm working"

def test_update_model_metrics():
    
    r = requests.put('http://localhost:8000/doc/update_model_metrics/10/', auth=HTTPBasicAuth('admin', 'mdp'))
    assert type(r.json()['coherence']) == float

def test_metrics():

    r = requests.post('http://localhost:8000/get_metrics', auth=HTTPBasicAuth('admin', 'mdp'))
    assert len(r.json()) == 3

def test_topic_from_new_text():
    data = {
  "file_name": "test_file",
  "file_content": "Mattia è un bimbo di 5 anni che passa tutte le sue giornate a disegnare. In realtà Mattia non si impegna più del necessario per tratteggiare le linee, fare bene le forme o rendere somiglianti le persone che disegna. Mattia ama soprattutto colorare, e ad ogni persona o cosa che disegna associa dei colori specifici. Ogni qual volta disegna suo papà Giuseppe, ad esempio, usa sempre gli stessi colori: i capelli li fa in nero, la maglia è azzurra e i pantaloni rigorosamente rossi. Il papà di Mattia non si veste ovviamente con colori così sgargianti, ma a Mattia piace immaginarlo così.",
  "date": "2001-05-03",
  "publication_name": "test",
  "publication_ref": "test"
}
    r = requests.put('http://localhost:8000/get_topic_from_new_text', json=data, auth=HTTPBasicAuth('admin', 'mdp'))
    assert type(r.json()['perplexity']) == float

def test_user():

    r = requests.put('http://localhost:8000/get_topic_from_new_text', auth=HTTPBasicAuth('fdmin', 'mdp'))
    assert r.json()['detail'] == 'Incorrect email or password'""", language='python' )

if page == pages[6]:

    st.markdown("<h1 style='text-align: center; color: white;'>Monitoring</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>AirFlow</h1>", unsafe_allow_html=True)
    st.write("""Graph view""")
    st.image('streamlit/streamlit_images/Graph_View.png', width = 1200)
    st.write("""Tree view""")
    st.image('streamlit/streamlit_images/Tree_View.png', width = 1200)


if page == pages[7]:


    st.markdown("<h1 style='text-align: center; color: white;'>Conclusion</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>Global Structure</h1>", unsafe_allow_html=True)
    st.image('streamlit/streamlit_images/architecture.jpeg',width=1200)
    #st.markdown("<h1 style='text-align: center; color: white;'>Outlooks</h1>", unsafe_allow_html=True)

if page == pages[8]:
    st.markdown("<h1 style='text-align: center; color: white;'>Web interface</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>Web Front</h1>", unsafe_allow_html=True)
    col1, col2, col3= st.columns([1,1,1])       
    with col1:                
    
      if st.button('API is working ?'): 
          r = requests.get('http://localhost:8000/')
          st.write(r.json())
    with col2:
      text_input = st.text_input("metrics for n random texts 👇")
      if text_input:
          n = text_input    
          r = requests.put("http://localhost:8000/doc/update_model_metrics/{n}/".format(n=n), auth=HTTPBasicAuth('admin', 'mdp'))
          #st.write(n)
          st.write(r.json())
    with col3:
        text_input = st.text_input("Type or paste some text 👇")
        if text_input:
          text = text_input
          data = {"file_name": "test_file", "file_content": text , "date": "2001-05-03",
          "publication_name": "test",
          "publication_ref": "test"
                  }
          r = requests.put('http://localhost:8000/get_topic_from_new_text', json=data, auth=HTTPBasicAuth('admin', 'mdp'))
          st.write(r.json())
        
    

