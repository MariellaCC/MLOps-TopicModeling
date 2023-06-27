
import streamlit as st
import pandas as pd 




#Page configuration 
st.set_page_config(page_title="Topic Modeling",page_icon='🌍',layout="wide", initial_sidebar_state="auto")

#Barre de Navigation 
st.sidebar.title('Navigation')
#Différentes pages du site 
pages = ['Introduction','Cahier des charges','ML et Version Contro','API','Base de données','Isolation' , 'Testing et Monitoring', 'Interface Graphique ']
page = st.sidebar.radio(' ',pages)

                                                    #Page 1: Introduction 
    
    
    
    
    
    
if page == pages[0]:
#Project Title
    st.markdown("<h1 style='text-align: center; color: green;'>Topic Modeling</h1>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: blue;'>DataScientest Project / MLOps FEV23</h2>", unsafe_allow_html=True)
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
    st.write("""
    Data Ingestion: 
    • Implement the data ingestion script (1_data_ingestion.py) as described earlier. 
    • Store the processed data in the database management system (e.g., MongoDB or HBase) instead of saving it to a CSV file. 
    • Ensure the database connection and table creation are handled appropriately within the script? 
    • Consider using an ORM (Object-Relational Mapping) library like SQLAlchemy to interact with the database ? \n
Pre-processing: 
• Implement the pre-processing script (2_pre_processing.py) to perform text pre-processing as described earlier. 
• Retrieve the data from the database management system instead of loading it from a CSV file.
• Update the script to store the pre-processed data back into the database, associating it with the respective records? \n
Model Training: 
• Implement the model training script (3_model_training.py) to train the LDA model as described earlier. 
• Modify the script to retrieve the pre-processed data from the database. 
• Store the trained LDA model in the MLflow tracking server using the MLflow Python API, providing the necessary metadata such as the experiment name and run parameters.\n
KPI Calculation: 
• Implement the KPI calculation script (4_kpi.py) to calculate the coherence value using the trained LDA model as described earlier. 
• Retrieve the trained LDA model from the MLflow tracking server using the MLflow Python API? • Perform the coherence calculation and print the result.\n
Airflow Integration:??? 
• Set up an Airflow DAG (Directed Acyclic Graph) to orchestrate the project workflow? 
• Define the tasks corresponding to each script (data ingestion, pre-processing, model training, and KPI calculation) as separate operators within the DAG? 
• Define the dependencies between the tasks to ensure the proper order of execution? • Use Airflow's scheduling capabilities to schedule the workflow execution at regular intervals or trigger it manually?\n
MLflow Integration:??? 
• Set up an MLflow tracking server to manage the model metadata and experiment runs
• Configure the MLflow tracking URI in the project scripts to connect to the tracking server. 
• Use MLflow's Python API to log the model parameters, metrics, and artifacts during the model training phase. 
• Retrieve the trained model and associated metadata from MLflow for KPI calculation and tracking.\n
Database Management System Integration:??? 
• Establish the connection to the selected database management system (e.g., MongoDB or HBase) in the project scripts. 
• Update the scripts to interact with the database for data ingestion, storage, and retrieval operations. • Utilize appropriate libraries or drivers (e.g., PyMongo for MongoDB) to facilitate database interactions.\n
Monitoring and Error Handling:??? 
• Implement logging and error handling mechanisms in the project scripts to capture relevant information and handle exceptions gracefully. 
• Utilize Airflow's built-in logging capabilities to track task execution and capture log outputs. Incorporate monitoring tools or services to monitor the deployed application, track performance metrics, and detect potential issues\n
API Development with FastAPI:??? 
• Create a new Python script to define the FastAPI application. 
• Use FastAPI to define the API endpoints that will interact with the trained model. 
• Implement an endpoint to accept input text data from the user and return the corresponding topic predictions using the trained LDA model. 
• Ensure the API endpoints perform the necessary data preprocessing and pass the preprocessed data to the LDA model for prediction. • Leverage the MLflow Python API to load the trained LDA model within the API script. 
• Provide appropriate input validation and error handling within the API endpoints. 
• Utilize FastAPI's automatic documentation generation to create an interactive API documentation accessible to users. \n
Dockerization:??? 
• Dockerize the entire project, including all the necessary dependencies and scripts, to create a portable and reproducible container image. 
• Write a Dockerfile to define the container environment and instructions for building the image. 
• Consider using a lightweight base image and installing the required dependencies (e.g., Python, MLflow, database drivers) within the Dockerfile. 
• Include the necessary scripts, such as the FastAPI application script and other project scripts, in the Docker image. \n
Kubernetes Deployment:??? 
• Deploy the Docker image to a Kubernetes cluster for scalable and reliable deployment. 
• Create Kubernetes manifests (e.g., Deployment, Service, Ingress) to define the desired deployment and expose the FastAPI service. 
• Specify resource requirements (CPU, memory) and scaling rules within the Kubernetes manifests to optimize resource allocation and handle increased traffic. 
• Consider utilizing Kubernetes features like horizontal pod autoscaling and rolling updates for better availability and resilience. \n
Continuous Integration and Deployment (CI/CD):?? 
• Set up a CI/CD pipeline to automate the building, testing, and deployment processes. 
• Configure a CI/CD tool (e.g., Jenkins, GitLab CI/CD, CircleCI) to monitor changes in the project repository and trigger the pipeline accordingly. 
• Define stages within the CI/CD pipeline, such as linting, unit testing, building Docker images, pushing images to a container registry, and deploying to the Kubernetes cluster. • Include appropriate testing steps, such as unit tests for the individual scripts, integration tests for the API endpoints, and performance/load testing for the deployed application. \n
    """)
    st.image('cdc.png', width = 1200)

if page == pages[3]:

    st.markdown("<h1 style='text-align: center; color: green;'>API</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; '>Présentation de l'API</h1>", unsafe_allow_html=True)
    st.write(""" 
    Entrée: 1 texte \n
    Sortie: topics & metrics
    
    """)
    st.markdown("<h2 style='text-align: center; '>Sécurité de l'API</h1>", unsafe_allow_html=True)
    st.write("blabblalba")
    st.markdown("<h2 style='text-align: center; '>Démo</h1>", unsafe_allow_html=True)
    st.write(""" http://localhost:8000/docs""")

if page == pages[4]:

    st.markdown("<h1 style='text-align: center; color: green;'>Base de données</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; '>SQL</h1>", unsafe_allow_html=True)
    st.write(""" 
    explication choix BDD
    
    """)
