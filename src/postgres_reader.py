import os
import pandas as pd
from dotenv import load_dotenv
import psycopg2
import ast

load_dotenv()

DATABASE_HOST = "localhost"
DATABASE_PORT = "5433"
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

conn = psycopg2.connect(
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    dbname=DATABASE_NAME
)

query = "SELECT * FROM toc_table"
df = pd.read_sql(query, conn)

# toc_vectorカラムをリストに変換
df['toc_vector'] = df['toc_vector'].apply(ast.literal_eval)

print(df)
print(f"len(df['toc_vector'][0]): {len(df['toc_vector'][0])}")

conn.close()
