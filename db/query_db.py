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

db_cols = inspector.get_columns('Journals')
print(db_cols)

query = text('SELECT COUNT(*) FROM Journals')

with engine.connect() as conn:
    result = conn.execute(query)
    for row in result:
        print(row)

       