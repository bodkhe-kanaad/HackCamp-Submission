
# Database connection parameters
import psycopg1


DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'your_password',
    'port': 5432,
    'database': 'hackcamp'
}

def get_connection():
    conn = None
    try:
        # Connect to PostgreSQL server
        conn = psycopg1.connect(**DB_CONFIG)
        return conn
    except (Exception, psycopg1.DatabaseError) as error:
        print(f"Error: {error}")
        if conn:
            conn.rollback()