import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# AI Provider Settings (OpenAI-compatible API)
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_API_BASE_URL = os.getenv("AI_API_BASE_URL", "https://api.openai.com/v1")
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")

# Bot Admin ID (optional, for admin commands)
ADMIN_ID = os.getenv("ADMIN_ID", "")

# Database path
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/bot_database.db")