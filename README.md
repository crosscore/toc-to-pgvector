# toc-to-pgvector

docker compose up --build -d

docker compose ps

docker compose exec pgvector_db bash

# pgvector環境のみを構築する場合
docker search pgvector
docker pull ankane/pgvector:latest

# もしくは手動でイメージをビルド
git clone --branch v0.7.2 https://github.com/pgvector/pgvector.git
cd pgvector
docker build --pull --build-arg PG_MAJOR=16 -t myuser/pgvector .

# pgvector拡張機能を有効化
CREATE EXTENSION IF NOT EXISTS vector;

# コンテナ外部から接続
psql -h localhost -U user -d toc_db -p 5432

# コンテナ内部から接続
psql -h pgvector_db -U user -d toc_db -p 5432

# .env
OPENAI_API_KEY=api_key
DB_NAME=toc_db
DB_USER=user
DB_PASSWORD=pass
DB_HOST=pgvector_db
DB_PORT=5432

5432（左側）: ホストマシン側のポート番号。ホストマシンは、このポートを通じて外部からの接続を受け付けます。この場合、ホストマシンの5432ポートでPostgreSQLデータベースにアクセスできるように設定されます。

5432（右側）: コンテナ内のポート番号。コンテナ内で実行されているPostgreSQLデータベースは、このポートを使用して接続を受け付けます。PostgreSQLのデフォルトポート番号は5432であり、この設定ではデフォルトポートを使用します。

# テーブルの中身を削除
TRUNCATE TABLE toc_table;

# テーブルの削除
DROP TABLE toc_table CASCADE;

# バージョン確認
SELECT version();
\dx

CREATE TABLE IF NOT EXISTS toc_table (
    id SERIAL PRIMARY KEY,
    file_name TEXT,
    toc TEXT,
    page INTEGER,
    toc_halfvec halfvec(3072)
);

CREATE INDEX ON toc_table USING hnsw (toc_halfvec halfvec_ip_ops);

\d+ documents
