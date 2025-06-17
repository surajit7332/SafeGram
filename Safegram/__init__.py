import logging
import time
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

boot_time = time.time()

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

Safegram = Client(
    ":Safegram:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    max_concurrent_transmissions=7,
    workers=50,
)

BOT_ID = None
BOT_USERNAME = None
BOT_NAME = None

async def initialize_bot():
    global BOT_ID, BOT_USERNAME, BOT_NAME

    await Safegram.start()
    me = await Safegram.get_me()

    BOT_ID = me.id
    BOT_USERNAME = me.username
    BOT_NAME = f"{me.first_name} {me.last_name}" if me.last_name else me.first_name
