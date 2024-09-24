import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from functools import lru_cache

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['PGHOST'],
        database=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        port=os.environ['PGPORT']
    )
    return conn

@lru_cache(maxsize=128)
def cached_query(query, params=None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(query, params)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def save_query(query, result):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO query_history (query, result) VALUES (%s, %s)",
            (query, json.dumps(result))
        )
        conn.commit()
    except Exception as e:
        print(f"Error saving query: {e}")
    finally:
        cur.close()
        conn.close()

def get_query_history(page=1, per_page=10):
    offset = (page - 1) * per_page
    query = """
    SELECT query, result
    FROM query_history
    ORDER BY created_at DESC
    LIMIT %s OFFSET %s
    """
    return cached_query(query, (per_page, offset))

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS query_history (
                id SERIAL PRIMARY KEY,
                query TEXT NOT NULL,
                result JSONB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_query_history_created_at
            ON query_history (created_at DESC)
        """)
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        cur.close()
        conn.close()

# Initialize the database when this module is imported
init_db()
