# toc-to-pgvector

docker-compose up --build -d

docker-compose ps

docker-compose exec vectorizer bash

docker-compose exec pgvector_db bash


# pgvector環境のみを構築する場合
docker search pgvector
docker pull ankane/pgvector:latest

# もしくは手動でイメージをビルド
git clone --branch v0.7.2 https://github.com/pgvector/pgvector.git
cd pgvector
docker build --pull --build-arg PG_MAJOR=16 -t myuser/pgvector .


# コンテナをバックグラウンドで起動
docker-compose up -d

# pgvector_dbコンテナに接続
docker-compose exec pgvector_db bash

# psqlコマンドを実行しデータベースに接続
psql -U db_user -d toc_db

# pgvector拡張機能を有効化
CREATE EXTENSION IF NOT EXISTS vector;

# pgvector_db以外からの接続
psql -h ${DATABASE_HOST} -U ${DATABASE_USER} -d ${DATABASE_NAME}
