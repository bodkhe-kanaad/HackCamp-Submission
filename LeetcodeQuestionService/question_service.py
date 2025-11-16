import random
from db import questions_collection

def get_random_question():
    total = questions_collection.count_documents({})
    if total == 0:
        return None
    idx = random.randint(0, total - 1)
    q = list(questions_collection.find().skip(idx).limit(1))[0]

    q["_id"] = str(q["_id"])
    # hide correct answer from students
    del q["correct_option"]

    return q

def check_answer(question_id, user_choice):
    q = questions_collection.find_one({"id": question_id})
    if not q:
        return None
    return q["correct_option"] == user_choice
