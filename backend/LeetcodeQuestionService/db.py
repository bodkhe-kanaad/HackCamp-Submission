from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["leetcode_quiz"]
questions_collection = db["questions"]