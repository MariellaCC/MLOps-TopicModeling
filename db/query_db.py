import pandas as pd
from sqlalchemy import URL, create_engine, inspect, text

url_object = URL.create(
    "mysql+pymysql",
    username="root",
    password="password",
    host="localhost",
    database="DB",
)

engine = create_engine(url_object)

inspector = inspect(engine)

# check columns that have been created
db_cols = inspector.get_columns('sources_train')
print(db_cols)

db_cols = inspector.get_columns('sources_test')
print(db_cols)

db_cols = inspector.get_columns('metrics')
print(db_cols)


# check length of dataset (must be equal to length of dataset as previously checked in database_creation.py)
query = text('SELECT COUNT(*) FROM sources_train')
with engine.connect() as conn:
    result = conn.execute(query)
    for row in result:
        print(row)

# check that query on date functions properly
date_ref_1 = "1897-1-1"
date_ref_2 = "1897-1-31"
query = text(f"SELECT * FROM sources_train WHERE date <= DATE '{date_ref_2}' AND date > DATE '{date_ref_1}'")
with engine.connect() as conn:
    result = conn.execute(query)
    for row in result:
        print(row)

# check that query on date functions properly
date_ref_1 = "1916-4-1"
date_ref_2 = "1916-4-30"
query = text(f"SELECT * FROM sources_test WHERE date <= DATE '{date_ref_2}' AND date > DATE '{date_ref_1}'")
with engine.connect() as conn:
    result = conn.execute(query)
    for row in result:
        print(row)

# check length of dataset (must be equal to length of dataset as previously checked in database_creation.py)
query = text('DESCRIBE metrics')
with engine.connect() as conn:
    result = conn.execute(query)
    for row in result:
        print(row)

       