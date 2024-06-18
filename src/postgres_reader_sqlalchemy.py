import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import ast

load_dotenv()

DB_NAME = "toc_db"
DB_USER = "user"
DB_PASSWORD = "pass"
DB_HOST = "localhost"
DB_PORT = "5432"

# SQLAlchemyエンジンの作成
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

query = "SELECT * FROM toc_table"
df = pd.read_sql(query, engine)

# toc_vectorカラムをリストに変換
df['toc_vector'] = df['toc_vector'].apply(ast.literal_eval)
print(df)

for i in range(10):
    print(len(df['toc_vector'][i]))
