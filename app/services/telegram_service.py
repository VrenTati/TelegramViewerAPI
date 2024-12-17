from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv
import os

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

SESSION_DIR = "sessions"
os.makedirs(SESSION_DIR, exist_ok=True)

def create_client(phone: str):
    session_path = os.path.join(SESSION_DIR, f"{phone}")
    client = TelegramClient(session_path, API_ID, API_HASH)

    return client

async def connect_telegram(phone: str):
    client = create_client(phone)
    await client.connect()

    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
        except Exception as e:
            raise ValueError(f"Failed to send code: {e}")

    return client

async def complete_login(client, phone: str, code: str, password: str = None):
    try:
        await client.sign_in(phone, code)
    except SessionPasswordNeededError:
        if not password:
            raise ValueError("This account requires a 2FA password.")
        await client.sign_in(password=password)

    return "Telegram account connected successfully!"

async def get_chats(client):
    chats = []
    async for dialog in client.iter_dialogs():
        chats.append({"id": dialog.id, "name": dialog.name})

    return chats

async def get_messages(client, chat_id: int, limit: int = 50):
    messages = []

    async for message in client.iter_messages(chat_id, limit=limit):
        messages.append({"id": message.id, "text": message.text})

    return messages

async def logout(client):
    await client.log_out()

    return "Logged out successfully!"


