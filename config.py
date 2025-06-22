import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ANYTHINGLLM_API_KEY = os.getenv("ANYTHINGLLM_API_KEY")
ANYTHINGLLM_BASE_URL = os.getenv("ANYTHINGLLM_BASE_URL")
WORKSPACE_SLUG = os.getenv("WORKSPACE_SLUG")

CACHE_FILE = 'user_threads_cache.pkl'