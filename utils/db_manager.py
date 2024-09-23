import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['PGHOST'],
        database=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        port=os.environ['PGPORT']
    )
    return conn

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

def get_query_history():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT query, result FROM query_history ORDER BY created_at DESC LIMIT 10")
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching query history: {e}")
        return []
    finally:
        cur.close()
        conn.close()

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
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        cur.close()
        conn.close()

# Initialize the database when this module is imported
init_db()
