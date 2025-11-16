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
    """Seed User, Pair, and Question tables with random data"""
    conn = None
    cursor = None
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Seed Question table first (5 sample questions)
        questions = [
            ("Complete the missing line in the Two Sum solution.\ndef twoSum(nums, target):\n    hashmap = {}\n    for i in range(len(nums)):\n        ### FILL HERE ###\n        hashmap[nums[i]] = i", "if nums[i] in hashmap: return [i, hashmap[nums[i]]]", "return [i, i + 1]", "if target - nums[i] in hashmap: return [hashmap[target - nums[i]], i]", "continue", "C"),
            ("Fill in the missing line to reverse the linked list.\ndef reverseList(head):\n    prev = None\n    curr = head\n    while curr:\n        ### FILL HERE ###\n        curr = nxt\n    return prev", "nxt = curr.next; curr.next = prev; prev = curr", "prev = curr.next", "nxt = prev", "curr = prev.next", "A"),
            ("Choose the correct condition to validate matching brackets.\ndef isValid(s):\n    stack = []\n    mapping = {')':'(', ']':'[', '}':'{'}\n    for c in s:\n        if c in mapping:\n            top = stack.pop() if stack else '#'\n            ### FILL HERE ###\n        else:\n            stack.append(c)\n    return not stack", "if not stack: return False", "if top != mapping[c]: return False", "stack.append(c)", "return True", "B"),
            ("Select the line that merges nodes in sorted order.\ndef mergeTwoLists(l1, l2):\n    dummy = ListNode(0)\n    curr = dummy\n    while l1 and l2:\n        ### FILL HERE ###\n    curr.next = l1 if l1 else l2\n    return dummy.next", "if l1.val <= l2.val: curr.next = l1; l1 = l1.next", "curr.next = None", "if l1 is None: break", "l2 = l1.next", "A"),
            ("Choose the correct pointer movement for binary search.\ndef search(nums, target):\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target:\n            return mid\n        ### FILL HERE ###\n    return -1", "right = mid - 1 if target < nums[mid] else right", "left = mid - 1", "right = mid + 1", "left = mid + 1 if target > nums[mid] else left; right = right", "A"),
        ]
        
        for q in questions:
            cursor.execute("""
                INSERT INTO "question" (question, A, B, C, D, correct_option)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, q)
        
        conn.commit()
        print(f"Seeded {len(questions)} questions successfully")
        
        # Insert 10 random users
        user_ids = []
        for i in range(10):
            username = generate_random_username()
            password = generate_random_password()
            interests = generate_random_array()
            courses = generate_random_array()
            
            cursor.execute("""
                INSERT INTO "users" (username, password, interests, courses, pair_id)
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
            question_id = random.randint(1, 5)
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
                UPDATE "users" SET pair_id = %s WHERE user_id IN (%s, %s)
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