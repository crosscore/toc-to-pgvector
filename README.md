# toc-to-pgvector

docker-compose up --build -d

docker-compose ps

docker-compose exec vectorizer_app bash

docker-compose exec postgresql_db bash



docker search pgvector

# Dockerイメージを取得
docker pull ankane/pgvector:latest

# もしくは手動でイメージをビルド
git clone --branch v0.7.2 https://github.com/pgvector/pgvector.git
cd pgvector
docker build --pull --build-arg PG_MAJOR=16 -t myuser/pgvector .
