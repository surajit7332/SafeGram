import asyncio
import importlib
from pyrogram import idle
from Safegram import Safegram, initialize_bot
from Safegram.modules import ALL_MODULES as MODULES
from Safegram.mongo import ALL_MODULES as MONGO_MODULES
from config import LOGGER_ID


async def start_bot():
    for mod in MODULES:
        try:
            importlib.import_module(f"Safegram.modules.{mod}")
        except Exception as err:
            print(f"❌ Error importing module '{mod}': {err}")
            raise

    for mongo_mod in MONGO_MODULES:
        try:
            importlib.import_module(f"Safegram.mongo.{mongo_mod}")
        except Exception as err:
            print(f"❌ Error importing mongo module '{mongo_mod}': {err}")
            raise

    await initialize_bot()

    await Safegram.send_message(
        LOGGER_ID,
        "**✅ ʙᴏᴛ ɪs ᴀʟɪᴠᴇ ᴀɴᴅ ᴅᴇᴘʟᴏʏᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
        "[ᴅᴇᴠᴇʟᴏᴘᴇʀ: JARVIS](https://t.me/certifiedcoder)",
        disable_web_page_preview=True
    )

    print("🤖 Bot Started Successfully. Awaiting events...")
    await idle()
    print("👋 Bot Stopped.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
