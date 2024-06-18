import psycopg2
import numpy as np
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import pandas as pd
import glob

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    openai_api_key=OPENAI_API_KEY,
)

def get_embedding(text):
    embedding = embeddings.embed_query(text)
    print("Embedding for text:", text, "is", embedding[:1], "... and more")
    return embedding

def normalize_vector(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

def save_vector_to_csv(vector, query_text, csv_file_path):
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        df = df[df['query_text'] != query_text]
    else:
        df = pd.DataFrame(columns=['query_text', 'query_vector'])

    new_data = pd.DataFrame({'query_text': [query_text], 'query_vector': [vector.tolist()]})
    df = pd.concat([df, new_data], ignore_index=True)

    df.to_csv(csv_file_path, index=False)
    print(f"Vector data saved to {csv_file_path}")

def get_vector_from_csv(csv_file_path, row_number):
    df = pd.read_csv(csv_file_path)
    if row_number < 0 or row_number >= len(df):
        raise ValueError("Invalid row number")
    query_vector = df.iloc[row_number]['query_vector']
    print(f"検索文字列：{df.iloc[row_number]['query_text']}")
    return np.array(eval(query_vector))

# # 類似検索を行う文章をベクトル化および正規化
# query_text = "犬の種類は？"
# normalize_query_vector = normalize_vector(get_embedding(query_text))

# # 新たに取得したベクトルデータをCSVに保存
# output_file_name = 'query_vector.csv'
# csv_file_path = os.path.join('../../data/csv/query_vector/', output_file_name)
# os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
# save_vector_to_csv(normalize_query_vector, query_text, csv_file_path)

# CSVファイルからベクトルを取得
csv_files = glob.glob('../../data/csv/query_vector/*.csv')
print(csv_files[0])
normalize_query_vector = get_vector_from_csv(csv_files[0], 0)

# PostgreSQLに接続
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host="localhost",
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

# 保存されているベクトルデータをチェック
# check_query = "SELECT id, toc_vector FROM toc_table LIMIT 5;"
# cursor.execute(check_query)
# stored_vectors = cursor.fetchall()
# for vector in stored_vectors:
#     print(f"Stored vector ID: {vector[0]}, Vector: {np.array(vector[1])}")

# 類似検索クエリの実行
similarity_search_query = """
SELECT file_name, toc, page, toc_vector, (toc_vector <-> %s::vector) AS distance
FROM toc_table
ORDER BY distance
LIMIT 5;
"""
cursor.execute(similarity_search_query, (normalize_query_vector.tolist(),))
results = cursor.fetchall()

# 検索結果の表示
if results:
    for result in results:
        file_name, toc, page, toc_vector, distance = result
        print(f"File: {file_name}, TOC: {toc}, Page: {page}, Distance: {distance}")
else:
    print("No results found")

cursor.close()
conn.close()
