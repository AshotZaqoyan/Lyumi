import aiohttp
import os
import pickle
import logging
from datetime import datetime
from config import ANYTHINGLLM_API_KEY, ANYTHINGLLM_BASE_URL, WORKSPACE_SLUG, CACHE_FILE
from responses import USER_ERROR_MSG

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class AnythingLLMManager:
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {ANYTHINGLLM_API_KEY}',
            'Content-Type': 'application/json'
        }
        self.user_threads = {}
        self.load_cache()

    def save_cache(self):
        try:
            with open(CACHE_FILE, 'wb') as f:
                pickle.dump({
                    'user_threads': self.user_threads,
                    'timestamp': datetime.now().isoformat()
                }, f)
            logging.info("Cache saved.")
        except Exception as e:
            logging.error(f"Error saving cache: {e}")

    def load_cache(self):
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'rb') as f:
                    data = pickle.load(f)
                    self.user_threads = data.get('user_threads', {})
                logging.info("Cache loaded.")
            except Exception as e:
                logging.error(f"Error loading cache: {e}")
        else:
            logging.info("No cache file found. Starting fresh.")

    async def recover_threads_from_workspace(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{ANYTHINGLLM_BASE_URL}/workspace/{WORKSPACE_SLUG}", headers=self.headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        threads = data.get("workspace", [{}])[0].get("threads", [])
                        for thread in threads:
                            slug = thread.get("slug")
                            if slug and slug.startswith("user-"):
                                user_id = slug.removeprefix("user-")
                                self.user_threads[user_id] = slug
                        self.save_cache()
                        logging.info(f"Recovered {len(self.user_threads)} threads from workspace API.")
                    else:
                        logging.warning(f"Failed to fetch workspace data: {resp.status}")
            except Exception as e:
                logging.error(f"Exception recovering threads: {e}")

    async def get_or_create_thread(self, user_id):
        if str(user_id) in self.user_threads:
            return self.user_threads[str(user_id)]

        slug = f"user-{user_id}"
        data = {'userId': 1, 'name': f'user_{user_id}', 'slug': slug}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f"{ANYTHINGLLM_BASE_URL}/workspace/{WORKSPACE_SLUG}/thread/new", headers=self.headers, json=data) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        self.user_threads[str(user_id)] = slug
                        self.save_cache()
                        return slug
                    elif resp.status == 400:
                        text = await resp.text()
                        if "Unique constraint failed" in text:
                            logging.info(f"Thread already exists for user {user_id}, attempting recovery.")
                            await self.recover_threads_from_workspace()
                            return self.user_threads.get(str(user_id), None)
                    error_text = await resp.text()
                    logging.error(f"Thread creation failed: {resp.status} - {error_text}")
            except Exception as e:
                logging.error(f"Error creating thread: {e}")
        return None

    async def send_message_to_thread(self, user_id, message):
        slug = await self.get_or_create_thread(user_id)
        if not slug:
            return USER_ERROR_MSG

        data = {'userId': 1, 'message': message, 'mode': 'chat'}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f"{ANYTHINGLLM_BASE_URL}/workspace/{WORKSPACE_SLUG}/thread/{slug}/chat", headers=self.headers, json=data) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        text_response = result.get('textResponse')
                        if not text_response:
                            logging.warning(f"No 'textResponse' field in API response for user {user_id}. Full response: {result}")
                            return USER_ERROR_MSG
                        return text_response
                    elif resp.status == 400:
                        logging.warning(f"Thread may be deleted or invalid. Recreating thread for user {user_id}.")
                        self.user_threads.pop(str(user_id), None)
                        await self.recover_threads_from_workspace()
                        return await self.send_message_to_thread(user_id, message)
                    error_text = await resp.text()
                    logging.error(f"Unexpected API response {resp.status} for user {user_id}: {error_text}")
                    return USER_ERROR_MSG
            except Exception as e:
                logging.error(f"Error sending message: {e}")
                return USER_ERROR_MSG