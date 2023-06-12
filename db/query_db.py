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
db_cols = inspector.get_columns('sources')
print(db_cols)

# check length of dataset (must be equal to length of dataset as previously checked in database_creation.py)
query = text('SELECT COUNT(*) FROM sources')
with engine.connect() as conn:
    result = conn.execute(query)
    for row in result:
        print(row)

# check that query on date functions properly
date_ref_1 = "1903-6-6"
date_ref_2 = "1903-6-29"
query = text(f"SELECT * FROM sources WHERE date <= DATE '{date_ref_2}' AND date > DATE '{date_ref_1}'")
with engine.connect() as conn:
    result = conn.execute(query)
    for row in result:
        print(row)

       