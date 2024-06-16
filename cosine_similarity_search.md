
# pgvector + コサイン類似度 + GINインデックスによる検索クエリの高速化

## 1. PostgreSQLとpgvectorのインストール

```bash
sudo apt-get install postgresql
psql -c "CREATE EXTENSION vector"
```

## 2. テーブルの作成

```sql
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    file_name TEXT,
    toc TEXT,
    page INTEGER,
    embedding vector(3072)
);
```

## 3. GINインデックスの作成（コサイン類似度用）

```sql
CREATE INDEX ON items USING gin (embedding vector_cosine_ops);
```

## 4. データの挿入

```sql
INSERT INTO items (embedding) VALUES (vector'[0.1, 0.2, ...]');
```

## 5. コサイン類似度検索の実行

```sql
SELECT * FROM items ORDER BY embedding <=> vector'[0.1, 0.2, ...]' LIMIT 10;
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
