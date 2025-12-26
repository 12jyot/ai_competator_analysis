from dotenv import load_dotenv
import os

load_dotenv()  # 🔥 loads .env ONCE

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found. Check .env file")
