
Commandes docker pour la mise en place de mysql: <br>

```
docker build -t local-mysql .
```
 <br>

```
docker run -dp 3306:3306 local-mysql
```
 <br>
L'installation des 3 packages suivants est nécessaire: SQLAlchemy, cryptography, PyMySQL. <br> <br>

Création de la base:

```
python database_creation.py
```

Tests sur la base: <br>

```
python query_db.py
```

 <br>
Tutoriel utilisé et adapté pour sqlalchemy:
https://www.learnpythonwithrune.org/how-to-setup-a-mysql-server-in-docker-for-your-python-project/

