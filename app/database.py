from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["ai_competitive_analysis"]

competitors_col = db["competitors"]
history_col = db["history"]
