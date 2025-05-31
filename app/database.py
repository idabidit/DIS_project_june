import psycopg2
import os

# Try to get from system enviroment variable
# Set your Postgres user and password as second arguments of these two next function calls
user = os.environ.get('PGUSER', 'postgres')
password = os.environ.get('PGPASSWORD', '0013')
host = os.environ.get('HOST', '127.0.0.1')
db = os.environ.get('PGDATABASE', 'pet_tinder_test')

def db_connection():
    db = "dbname='pet_tinder_test' user=" + user + " host=" + host + " password =" + password
    conn = psycopg2.connect(db)

    return conn

def init_db():
    try:
        conn = db_connection()
        cur = conn.cursor()
        
        # Execute schema.sql
        with open('schema.sql', 'r') as f:
            cur.execute(f.read())
        
        conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
        raise e
    finally:
        cur.close()
        conn.close()