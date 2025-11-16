import db
import psycopg2
import random
import string

DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'your_password',
    'port': 5432,
    'database': 'hackcamp'
}


def generate_random_username():
    """Generate random username"""
    return ''.join(random.choices(string.ascii_lowercase, k=8))


def generate_random_password():
    """Generate random password"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))


def generate_random_array():
    """Generate random array of strings"""
    categories = ['math', 'science', 'history', 'art', 'music', 'sports', 'coding', 'writing']
    return random.sample(categories, random.randint(1, 4))


def seed_data():
    """Seed User and Pair tables with random data"""
    conn = None
    cursor = None
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Insert 10 random users
        user_ids = []
        for i in range(10):
            username = generate_random_username()
            password = generate_random_password()
            interests = generate_random_array()
            courses = generate_random_array()
            
            cursor.execute("""
                INSERT INTO "User" (username, password, interests, courses, pair_id)
                VALUES (%s, %s, %s, %s, NULL)
                RETURNING user_id
            """, (username, password, interests, courses))
            
            user_id = cursor.fetchone()[0]
            user_ids.append(user_id)
        
        conn.commit()
        print(f"Seeded {len(user_ids)} random users successfully")
        
        # Insert 5 random pairs
        pair_ids = []
        for i in range(5):
            user1 = random.choice(user_ids)
            user2 = random.choice([u for u in user_ids if u != user1])
            streak = random.randint(0, 100)
            question_id = random.randint(1, 50)
            user1_answered = random.choice([True, False])
            user2_answered = random.choice([True, False])
            
            cursor.execute("""
                INSERT INTO "Pair" (user1, user2, streak, question_id, user1_answered, user2_answered)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING pair_id
            """, (user1, user2, streak, question_id, user1_answered, user2_answered))
            
            pair_id = cursor.fetchone()[0]
            pair_ids.append(pair_id)
            
            # Update users with pair_id
            cursor.execute("""
                UPDATE "User" SET pair_id = %s WHERE user_id IN (%s, %s)
            """, (pair_id, user1, user2))
        
        conn.commit()
        print(f"Seeded {len(pair_ids)} random pairs successfully")
        
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
    seed_data()