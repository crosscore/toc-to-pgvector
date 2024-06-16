import numpy as np
import pandas as pd
import glob

def normalize_vector(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

# 表示精度の設定
np.set_printoptions(precision=17)

file_paths = glob.glob("../data/csv/vector/*.csv")
df = pd.read_csv(file_paths[0])

# ベクトルの文字列を数値の配列に変換
embedding_vector_str = df['toc(vector)'][0]
embedding_vector = np.fromstring(embedding_vector_str.strip('[]'), sep=',')

# ベクトルの正規化
normalized_vector = normalize_vector(embedding_vector)
print("Normalized vector:", normalized_vector)

# 正規化後のベクトルのノルムを計算
norm_of_normalized_vector = np.linalg.norm(normalized_vector)
print("Norm of normalized vector:", norm_of_normalized_vector)
