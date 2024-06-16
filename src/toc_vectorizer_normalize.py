import pandas as pd
import os
import glob
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import numpy as np

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    openai_api_key=OPENAI_API_KEY,
)

input_directory = '../data/csv/original/'
output_directory = '../data/csv/vector/'
os.makedirs(output_directory, exist_ok=True)

# ベクトル化する列名の定義
column_to_vectorize = 'toc'
vectorized_column_name = column_to_vectorize + '_vector'

# 入力ディレクトリ内の全CSVファイルを取得
csv_files = glob.glob(os.path.join(input_directory, '*.csv'))
print(f"Found CSV files: {csv_files}")

def get_embedding(text):
    embedding = embeddings.embed_query(text)
    print(f"Embedding for text: {text} is {embedding[:1]} ... and more")
    return embedding

def normalize_vector(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

# 各CSVファイルに対して処理を実行
for input_file_path in csv_files:
    print(f"Processing file: {input_file_path}")
    output_file_path = os.path.join(output_directory, os.path.splitext(os.path.basename(input_file_path))[0] + '_vectorized.csv')

    df = pd.read_csv(input_file_path)
    print(f"DataFrame loaded: {df.head()}")

    # ベクトル化および正規化された配列を格納した列を追加
    df[vectorized_column_name] = df[column_to_vectorize].apply(lambda x: normalize_vector(get_embedding(x)).tolist())

    df.to_csv(output_file_path, index=False)
    print(f"File saved: {output_file_path}")
