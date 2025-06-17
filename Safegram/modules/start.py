from pyrogram import filters
import time, platform, psutil
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Safegram import Safegram, BOT_USERNAME
from Safegram.modules.utils import time_formatter, size_formatter

# -- Constants --
START_TEXT = """<b>🤖 ᴄᴏᴘʏʀɪɢʜᴛ & ᴄᴘ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ʙᴏᴛ 🛡️</b>

ʜᴇʏ ᴛʜᴇʀᴇ! ɪ'ᴍ ʏᴏᴜʀ ɢʀᴏᴜᴘ'ꜱ ᴇɴғᴏʀᴄᴇʀ ʀᴏʙᴏᴛ 🤖  
ᴍʏ ᴍɪssɪᴏɴ ɪs ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ ᴄᴏᴍᴍᴜɴɪᴛʏ ғʀᴏᴍ:

• ғᴀᴋᴇ ᴄᴏᴘʏʀɪɢʜᴛ ʀᴇᴘᴏʀᴛs 🚫  
• ᴄʜɪʟᴅ ᴇxᴘʟᴏɪᴛᴀᴛɪᴏɴ ᴄᴏɴᴛᴇɴᴛ ❌  
• ʟᴏɴɢ ᴀɴᴅ sᴜsᴘɪᴄɪᴏᴜs ᴇᴅɪᴛᴇᴅ ᴍᴇssᴀɢᴇs 📝  
• ɢʀᴏᴜᴘ sᴘᴀᴍ & ɪɴᴛʀᴜsɪᴏɴ 🔐

➥ ʜᴏᴡ ᴛᴏ ᴇɴᴀʙʟᴇ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ:
1. ➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ  
2. 🛡️ ɢʀᴀɴᴛ ᴍᴇ ᴀᴅᴍɪɴ ᴘᴇʀᴍɪssɪᴏɴs

ᴏɴᴄᴇ ᴇɴᴀʙʟᴇᴅ, ɪ'ʟʟ ᴄᴏɴᴛɪɴᴜᴏᴜsʟʏ ᴍᴏɴɪᴛᴏʀ ᴀɴᴅ ᴀᴄᴛ ᴛᴏ ᴋᴇᴇᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ sᴀғᴇ ✅

<b><a href="https://t.me/SafeGramRobot">ꜱᴀꜰᴇɢʀᴀᴍʀᴏʙᴏᴛ</a> — ʏᴏᴜʀ ᴅɪɢɪᴛᴀʟ ꜰɪʀᴇᴡᴀʟʟ 🔒</b>
"""

# -- Handlers --
@Safegram.on_message(filters.command("start"))
async def start_command_handler(_, msg):
    buttons = [
        [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [InlineKeyboardButton("• ʜᴀɴᴅʟᴇʀ •", callback_data="vip_back")]
    ]
    await msg.reply_photo(
        photo="https://telegra.ph/file/8f6b2cc26b522a252b16a.jpg",
        caption=START_TEXT,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

start_time = time.time()

@Safegram.on_message(filters.command("ping"))
async def activevc(_, message: Message):
    uptime = time_formatter((time.time() - start_time) * 1000)
    cpu = psutil.cpu_percent()
    storage = psutil.disk_usage('/')
    python_version = platform.python_version()

    await message.reply_text(
        f"🏓 **ᴘᴏɴɢ ʀᴇsᴘᴏɴsᴇ!**\n\n"
        f"➪ **ᴜᴘᴛɪᴍᴇ:** {uptime}\n"
        f"➪ **ᴄᴘᴜ:** {cpu}%\n"
        f"➪ **ᴅɪsᴋ:** {size_formatter(storage.used)} / {size_formatter(storage.total)}\n"
        f"➪ **ғʀᴇᴇ:** {size_formatter(storage.free)}\n"
        f"➪ **ᴘʏᴛʜᴏɴ:** {python_version}",
        quote=True
    )
