# MLOps - Topic Modeling

## About the project 
The project MLOps - Topic Modeling aims at deploying a topic modeling workflow with an MLOps approach.<br>
As an underlying workflow, we selected the project <i>Topic Modelling with Gensim. A workflow for the Humanities</i> available under the following repo: https://github.com/DHARPA-Project/TopicModelling- (1). The reference materials that we used were forked into the "reference" directory of the current project.

## Metrics and performance requirements


## Implementation scheme

1. Data Ingestion:
• Implement the data ingestion script (1_data_ingestion.py) as described earlier.
• Store the processed data in the database management system (MySQL) instead of saving it to a CSV file.
• Ensure the database connection and table creation are handled appropriately within the script.
• Use of an ORM (Object-Relational Mapping) library like SQLAlchemy to interact with the database.
2. Pre-processing:
• Implement the pre-processing script (2_pre_processing.py) to perform text pre-processing as described earlier.
• Retrieve the data from the database management system instead of loading it from a CSV file.
• Update the script to store the pre-processed data back into the database, associating it with the respective records?
3. Model Training:
• Implement the model training script (3_model_training.py) to train the LDA model as described earlier.
• Modify the script to retrieve the pre-processed data from the database.
• Store the trained LDA model in the MLflow tracking server using the MLflow Python API, providing the necessary metadata such as the experiment name and run parameters.
4. KPI Calculation:
• Implement the KPI calculation script (4_kpi.py) to calculate the coherence value using the trained LDA model as described earlier.
• Retrieve the trained LDA model from the MLflow tracking server using the MLflow Python API?
• Perform the coherence calculation and print the result.
5. Airflow Integration:
• Set up an Airflow DAG (Directed Acyclic Graph) to orchestrate the project workflow for model retraining if metrics are not ok.
• Define the tasks corresponding to each script (data ingestion, pre-processing, model retraining, and KPI calculation) as separate operators within the DAG.
• Define the dependencies between the tasks to ensure the proper order of execution: if KPI not okay then relaunch from data ingestion to retraining.
6. Database Management System Integration:
• Establish the connection to the selected database management system in the project scripts.
• Update the scripts to interact with the database for data ingestion, storage, and retrieval operations.
7. API Development with FastAPI:
• Create a new Python script to define the FastAPI application.
• Use FastAPI to define the API endpoints that will interact with the trained model.
• Implement an endpoint to accept input text data from the user and return the corresponding topic predictions using the trained LDA model.
• Ensure the API endpoints perform the necessary data preprocessing and pass the preprocessed data to the LDA model for prediction.
8. Dockerization:
• Dockerize the entire project, including all the necessary dependencies and scripts, to create a portable and reproducible container image.
• Write a Dockerfile to define the container environment and instructions for building the image.
• Consider using a lightweight base image and installing the required dependencies (e.g., Python, MySQL database drivers) within the Dockerfile.
• Include the necessary scripts, such as the FastAPI application script and other project scripts, in the Docker image.
• Docker Compose everything. 
9. Continuous Integration and Deployment (CI/CD):
• Set up a CI/CD pipeline to automate the building, testing, and deployment processes with Github actions.


![markmap](https://github.com/MariellaCC/MLOps-TopicModeling/assets/83060092/e9edd822-2837-47b1-824d-acdc8ed63d2e)

## Implementation Logical Worflow: Technical Architecture 

![MLOps Topic Modeling Diagram](https://github.com/MariellaCC/MLOps-TopicModeling/assets/83060092/59550731-6359-4a68-a777-c4fbe51a8e2e)


## References

1. Viola, Lorella and de Crouy-Chanel, Mariella. 2020. Topic Modelling with Gensim. A workflow for the Humanities (v. 1.0.0). University of Luxembourg. https://github.com/DHARPA-Project/TopicModelling-
