import os
import psycopg2
from psycopg2 import sql, Error
from dotenv import load_dotenv

load_dotenv()

# データベース接続
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host="localhost",
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

# テーブルを完全に削除
drop_table_query = sql.SQL("DROP TABLE {} CASCADE").format(sql.Identifier('toc_table'))

try:
    cursor.execute(drop_table_query)
    conn.commit()
    print("テーブルのデータが完全に削除されました。")
except Error as e:
    if e.pgcode == '42P01':  # Undefined table
        print("エラー: テーブル 'toc_table' は存在しません。")
    else:
        print(f"エラーが発生しました: {e}")
finally:
    cursor.close()
    conn.close()
