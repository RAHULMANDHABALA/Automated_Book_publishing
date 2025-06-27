import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Playwright settings
    HEADLESS = True
    SCREENSHOT_DIR = "screenshots"
    
    # Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    WRITER_TEMPERATURE = 0.7
    REVIEWER_TEMPERATURE = 0.3
    
    # ChromaDB
    DB_PATH = "chroma_db"
    COLLECTION_NAME = "book_versions"
    
    # RL Search
    SEARCH_LEARNING_RATE = 0.01
    SEARCH_MEMORY_SIZE = 1000