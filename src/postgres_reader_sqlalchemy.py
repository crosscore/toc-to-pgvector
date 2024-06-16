import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import ast

load_dotenv()

DATABASE_HOST = "localhost"
DATABASE_PORT = "5433"
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# SQLAlchemyエンジンの作成
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
engine = create_engine(DATABASE_URL)

query = "SELECT * FROM toc_table"
df = pd.read_sql(query, engine)

# toc_vectorカラムをリストに変換
df['toc_vector'] = df['toc_vector'].apply(ast.literal_eval)

print(df)
print(f"len(df['toc_vector'][0]): {len(df['toc_vector'][0])}")

print(df['toc_vector'][0])
