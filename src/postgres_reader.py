import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv
import ast

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host="localhost",
    port=os.getenv("DB_PORT")
)

query = "SELECT * FROM toc_table;"
df = pd.read_sql_query(query, conn)
print(df)

# toc_vectorカラムをリストに変換
df['toc_vector'] = df['toc_vector'].apply(ast.literal_eval)

print(len(df['toc_vector'][0]))
print(len(df['toc_vector'][1]))
print(len(df['toc_vector'][2]))
conn.close()
