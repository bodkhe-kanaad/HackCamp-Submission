import db
import psycopg2
import random
import string
from faker import Faker

fake = Faker()

DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'your_password',
    'port': 5432,
    'database': 'hackcamp'
}


def generate_random_username():
    """Generate random username using Faker"""
    return fake.user_name()


def generate_random_password():
    """Generate random password"""
    return fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)


def generate_random_array():
    """Generate random array of strings"""
    interests = ['Video Games', 'Sport', 'Coding', 'Hiking', 'Party']
    return random.sample(interests, random.randint(1, 4))


def generate_random_courses():
    """Generate random array of course strings"""
    courses = ['CPSC 110', 'CPSC 210', 'CPSC 310', 'CPSC 221', 'CPSC 320', 'MATH 100', 'MATH 101', 'HIST 101', 'HIST 102', 'BIOL 111', 'BIOL 121', 'CHEM 121', 'CHEM 123']
    return random.sample(courses, random.randint(1, 4))


def seed_data():
    """Seed User, Pair, and Question tables with random data"""
    conn = None
    cursor = None
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Seed Question table first (5 sample questions)
        questions = [
            ("Complete the missing line in the Two Sum solution.\ndef twoSum(nums, target):\n    hashmap = {}\n    for i in range(len(nums)):\n        ### FILL HERE ###\n        hashmap[nums[i]] = i", "if nums[i] in hashmap: return [i, hashmap[nums[i]]]", "return [i, i + 1]", "if target - nums[i] in hashmap: return [hashmap[target - nums[i]], i]", "continue", "C", "leetcode"),
            ("Fill in the missing line to reverse the linked list.\ndef reverseList(head):\n    prev = None\n    curr = head\n    while curr:\n        ### FILL HERE ###\n        curr = nxt\n    return prev", "nxt = curr.next; curr.next = prev; prev = curr", "prev = curr.next", "nxt = prev", "curr = prev.next", "A", "leetcode"),
            ("Choose the correct condition to validate matching brackets.\ndef isValid(s):\n    stack = []\n    mapping = {')':'(', ']':'[', '}':'{'}\n    for c in s:\n        if c in mapping:\n            top = stack.pop() if stack else '#'\n            ### FILL HERE ###\n        else:\n            stack.append(c)\n    return not stack", "if not stack: return False", "if top != mapping[c]: return False", "stack.append(c)", "return True", "B", "leetcode"),
            ("Select the line that merges nodes in sorted order.\ndef mergeTwoLists(l1, l2):\n    dummy = ListNode(0)\n    curr = dummy\n    while l1 and l2:\n        ### FILL HERE ###\n    curr.next = l1 if l1 else l2\n    return dummy.next", "if l1.val <= l2.val: curr.next = l1; l1 = l1.next", "curr.next = None", "if l1 is None: break", "l2 = l1.next", "A", "leetcode"),
            ("Choose the correct pointer movement for binary search.\ndef search(nums, target):\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target:\n            return mid\n        ### FILL HERE ###\n    return -1", "right = mid - 1 if target < nums[mid] else right", "left = mid - 1", "right = mid + 1", "left = mid + 1 if target > nums[mid] else left; right = right", "A", "leetcode"),
        ]
        
        for q in questions:
            cursor.execute("""
                INSERT INTO "question" (question, A, B, C, D, correct_option, source_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, q)
        
        conn.commit()
        print(f"Seeded {len(questions)} questions successfully")
        
        # Insert 30 random users (20 paired, 10 unpaired)
        user_ids = []
        num_users = 30
        for i in range(num_users):
            username = generate_random_username()
            password = generate_random_password()
            interests = generate_random_array()
            courses = generate_random_courses()
            
            cursor.execute("""
                INSERT INTO "users" (username, password, interests, courses, pair_id)
                VALUES (%s, %s, %s, %s, NULL)
                RETURNING user_id
            """, (username, password, interests, courses))
            
            user_id = cursor.fetchone()[0]
            user_ids.append(user_id)
        
        conn.commit()
        print(f"Seeded {len(user_ids)} random users successfully")
        
        # Insert 10 random pairs (first 20 users paired, last 10 unpaired)
        pair_ids = []
        num_pairs = 10
        for i in range(num_pairs):
            user1 = user_ids[i * 2]
            user2 = user_ids[i * 2 + 1]
            streak = random.randint(0, 100)
            # 60% chance to have a question, 40% chance to be NULL
            # question ids now range from 1..len(questions)
            question_id = random.randint(1, len(questions)) if random.random() < 0.6 else None
            user1_answered = random.choice([True, False])
            user2_answered = random.choice([True, False])
            ai_mode = random.choice([True, False])
            
            cursor.execute("""
                INSERT INTO "Pair" (user1, user2, streak, question_id, user1_answered, user2_answered, ai_mode)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING pair_id
            """, (user1, user2, streak, question_id, user1_answered, user2_answered, ai_mode))
            
            pair_id = cursor.fetchone()[0]
            pair_ids.append(pair_id)
            
            # Update users with pair_id
            cursor.execute("""
                UPDATE "users" SET pair_id = %s WHERE user_id IN (%s, %s)
            """, (pair_id, user1, user2))
        
        conn.commit()
        print(f"Seeded {len(pair_ids)} random pairs successfully")
        print(f"{num_users - num_pairs*2} users remain unpaired")
        
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