import numpy as np

def normalize_vector(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

embedding_vector = np.array([0.3, -0.4, 0.5])

# ベクトルの正規化
normalized_vector = normalize_vector(embedding_vector)
print("Normalized vector:", normalized_vector)

# 正規化後のベクトルの配列を全て合計した値を計算
sum_of_normalized_vector = np.sum(normalized_vector)
print("Sum of normalized vector:", sum_of_normalized_vector)

# 正規化後のベクトルのノルムを計算
norm_of_normalized_vector = np.linalg.norm(normalized_vector)
print("Norm of normalized vector:", norm_of_normalized_vector)
