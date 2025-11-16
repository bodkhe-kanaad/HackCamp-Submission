import db
import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'your_password',
    'port': 5432
}


def create_database_and_tables():
    """Create database and User and Pair tables"""
    conn = None
    cursor = None
    
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(**DB_CONFIG)
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
        
        # Create Pair table first (no foreign keys)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "Pair" (
                pair_id SERIAL PRIMARY KEY,
                user1 INTEGER,
                user2 INTEGER,
                streak INTEGER DEFAULT 0,
                question_id INTEGER DEFAULT NULL,
                user1_answered BOOLEAN DEFAULT FALSE,
                user2_answered BOOLEAN DEFAULT FALSE
            );
        """)
        
        # Create User table with foreign key to Pair
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "users" (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                interests VARCHAR(255)[] DEFAULT '{}',
                courses VARCHAR(255)[] DEFAULT '{}',
                pair_id INTEGER REFERENCES "Pair"(pair_id) ON DELETE SET NULL
            );
        """)
        
        # Add foreign key constraints to Pair table
        cursor.execute("""
            ALTER TABLE "Pair"
            ADD CONSTRAINT fk_pair_user1 FOREIGN KEY (user1) REFERENCES "User"(user_id) ON DELETE SET NULL,
            ADD CONSTRAINT fk_pair_user2 FOREIGN KEY (user2) REFERENCES "User"(user_id) ON DELETE SET NULL;
        """)
        
        conn.commit()
        print("Tables 'User' and 'Pair' created successfully")
        
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