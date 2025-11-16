import db
import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'your_password',
    'port': 5432
}


def create_database_and_tables():
    """Create database and User table"""
    conn = None
    cursor = None
    
    try:
        # Connect to PostgreSQL server
        conn = db.get_connection()
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("DROP DATABASE IF EXISTS hackcamp;")
        cursor.execute("CREATE DATABASE hackcamp;")
        print("Database 'hackcamp' created successfully")
        
        conn.close()
        
        # Connect to the new database
        DB_CONFIG['database'] = 'hackcamp'
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Create User table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "User" (
                UserId SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                interests VARCHAR(255)[] DEFAULT '{}',
                courses VARCHAR(255)[] DEFAULT '{}',
                answered_q BOOLEAN NOT NULL DEFAULT FALSE,
                partnerId INTEGER REFERENCES "User"(UserId) ON DELETE SET NULL,
                question_id INTEGER
            );
        """)
        
        conn.commit()
        print("Table 'User' created successfully")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        if conn:
            conn.rollback()
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database_and_tables()