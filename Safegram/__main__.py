import asyncio
import importlib
from pyrogram import idle
from Safegram import Safegram, initialize_bot
from Safegram.modules import ALL_MODULES
from config import LOGGER_ID

async def start_bot():
    for module in ALL_MODULES:
        importlib.import_module(f"Safegram.modules.{module}")

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
