import pandas as pd
import os
import glob
from dotenv import load_dotenv
import psycopg2
import ast

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT")
)
cursor = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS toc_table (
    id SERIAL PRIMARY KEY,
    file_name TEXT,
    toc TEXT,
    page INTEGER,
    toc_vector vector(3072)
);
"""
cursor.execute(create_table_query)
conn.commit()

input_directory = '../data/csv/vector/'
csv_files = glob.glob(os.path.join(input_directory, '*.csv'))
print(f"Found CSV files: {csv_files}")

# 全CSVファイルに対してベクトル化の処理を実行
for input_file_path in csv_files:
    df = pd.read_csv(input_file_path)

    # ベクトルデータをPostgreSQLに挿入
    for index, row in df.iterrows():
        try:
            print(f"Inserting row: {row}")

            # ベクトルをリスト形式に変換
            toc_vector = ast.literal_eval(row['toc_vector'])

            insert_query = """
            INSERT INTO toc_table (file_name, toc, page, toc_vector)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_query, (row['file_name'], row['toc'], row['page'], toc_vector))
            print("Row inserted")
        except Exception as e:
            print(f"Error inserting row: {e}")

    conn.commit()

cursor.close()
conn.close()
