
# HNSW + GINによる類似検索の高速化

## 1. PostgreSQLとpgvectorのインストール

### a. Dockerを使用する場合

```bash
docker pull ankane/pgvector:latest
docker run -d -p 5432:5432 --name pgvector -e POSTGRES_PASSWORD=mysecretpassword ankane/pgvector:latest
```

### b. ローカルインストールの場合

```bash
sudo apt-get install postgresql
psql -c "CREATE EXTENSION vector"
```

## 2. テーブルの作成

```sql
CREATE TABLE items (
    id serial PRIMARY KEY,
    file_name TEXT,
    toc TEXT,
    page INTEGER,
    toc_vector vector(3072)
);
```

## 3. HNSWインデックスの作成

```sql
CREATE INDEX ON items USING hnsw (toc_vector);
```

## 4. GINインデックスの作成

```sql
CREATE INDEX ON items USING gin (toc_vector vector_l2_ops);
```

## 5. データの挿入

```sql
INSERT INTO items (file_name, toc, page, toc_vector) VALUES
('document1.pdf', 'Introduction to HNSW', 1, vector'[0.1, 0.2, ...]'),
('document2.pdf', 'Advanced HNSW Techniques', 2, vector'[0.3, 0.4, ...]');
```

## 6. HNSW + GINによる類似検索の実行

```sql
SELECT * FROM items
WHERE toc_vector @> 'フィルタ条件'
ORDER BY toc_vector <=> vector'[0.1, 0.2, ...]'
LIMIT 10;
```

## インデックスの確認

### 1. `\d+` コマンドを使用（psqlシェルの場合）

```sql
\d+ items
```

### 2. `pg_indexes` ビューを使用

```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'items';
```
