from __future__ import annotations

import time
import platform
import psutil

from pyrogram import filters
from pyrogram.enums import ParseMode, ChatType
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from config import LOGGER_ID
from Safegram import Safegram, BOT_USERNAME
from Safegram.modules.utils import time_formatter, size_formatter
from Safegram.mongo.usersdb import add_user, get_all_users
from Safegram.mongo.chatsdb import get_all_chats

START_TEXT = """<b><a href="https://t.me/YourBotUsername">ᴜsᴇʀ ᴛᴀɢɢᴇʀ ʙᴏᴛ 🏷️</a></b>



ʜᴇʏ! ɪ'ᴍ ʏᴏᴜʀ ɢʀᴏᴜᴘ'ꜱ ᴇɴɢᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ✨
ᴍʏ ᴍɪssɪᴏɴ ɪs ᴛᴏ ᴍᴇɴᴛɪᴏɴ & ɴᴏᴛɪғʏ ᴇᴠᴇʀʏᴏɴᴇ ɪɴ sᴛʏʟᴇ:

• ᴛᴀɢ ᴀʟʟ ᴍᴇᴍʙᴇʀꜱ 👥
• ᴛᴀɢ ᴀᴅᴍɪɴs ᴏɴʟʏ 🛡️
• ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ / ɢᴏᴏᴅ ɴɪɢʜᴛ ᴛᴀɢ 🌅🌙
• ʀᴀɴᴅᴏᴍ ʜɪᴛ & ʟɪғᴇ ǫᴜᴏᴛᴇ ᴛᴀɢ 🎯💫

➥ ʜᴏᴡ ᴛᴏ ᴜꜱᴇ:
1. ➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ
2. 🛡️ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ꜱᴛᴀʀᴛ ᴛᴀɢɢɪɴɢ
3. 💬 ᴜꜱᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ʟɪᴋᴇ `/utag`, `/admintag`, `/gmhit`, `/gntag`

ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ, ᴄʟɪᴄᴋ ᴛʜᴇ **ʜᴇʟᴘ** ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ⬇️

<b><a href="https://t.me/ThePriyanshuOp">ᴏᴡɴᴇʀ</a> — ᴏꜰꜰɪᴄɪᴀʟ ʙᴏᴛ ᴏᴡɴᴇʀ 👑</b>
<b><a href="https://t.me/best_friends_chatting_grpz0">ꜱᴜᴘᴘᴏʀᴛ</a> — ɢᴇᴛ ʜᴇʟᴘ & ᴀꜱꜱɪꜱᴛᴀɴᴄᴇ 🛠️</b>
"""

HELP_TEXT = """<b>🔖 ʜᴇʟᴘ ᴍᴇɴᴜ</b>

🧩 ʜᴇʟᴘ ᴍᴇɴᴜ

• /ping – ʙᴏᴛ ꜱᴛᴀᴛᴜꜱ
• /stats – ᴜꜱᴀɢᴇ ᴅᴀᴛᴀ
• /utag – ᴛᴀɢ ᴀʟʟ ᴍᴇᴍʙᴇʀꜱ
• /admintag – ᴛᴀɢ ᴀʟʟ ᴀᴅᴍɪɴꜱ
• /gmtag – ᴛᴀɢ ᴡɪᴛʜ ʀᴀɴᴅᴏᴍ ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ᴍᴇꜱꜱᴀɢᴇ
• /gntag – ᴛᴀɢ ᴡɪᴛʜ ʀᴀɴᴅᴏᴍ ɢᴏᴏᴅ ɴɪɢʜᴛ ᴍᴇꜱꜱᴀɢᴇ
• /hitag – ᴛᴀɢ ᴡɪᴛʜ ʀᴀɴᴅᴏᴍ ʜɪᴛ ᴍᴇꜱꜱᴀɢᴇ
• /lifetag – ᴛᴀɢ ᴡɪᴛʜ ʀᴀɴᴅᴏᴍ ʟɪꜰᴇ ǫᴜᴏᴛᴇ
• /gmstop – ꜱᴛᴏᴘ ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ᴛᴀɢɢɪɴɢ
• /gnstop – ꜱᴛᴏᴘ ɢᴏᴏᴅ ɴɪɢʜᴛ ᴛᴀɢɢɪɴɢ
• /histop – ꜱᴛᴏᴘ ʜɪᴛ ᴛᴀɢɢɪɴɢ
• /cancel – ꜱᴛᴏᴘ /utag ᴀɴᴅ /admintag ᴘʀᴏᴄᴇꜱꜱ
"""

start_time = time.time()

def get_main_buttons() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
            InlineKeyboardButton("🧩 ʜᴇʟᴘ", callback_data="show_help")
        ],
        [
            InlineKeyboardButton("🛠️ sᴜᴘᴘᴏʀᴛ", url="https://t.me/best_friends_chatting_grpz0"),
            InlineKeyboardButton("🌀 ᴜᴘᴅᴀᴛᴇ", url="https://t.me/NeoUpdatess"),
        ],
    ])

def get_ping_stats_buttons() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛠️ sᴜᴘᴘᴏʀᴛ", url="https://t.me/best_friends_chatting_grpz0"),
            InlineKeyboardButton("🌀 ᴜᴘᴅᴀᴛᴇ", url="https://t.me/NeoUpdatess"),
        ]
    ])

@Safegram.on_message(filters.command("start"))
async def start_command_handler(_, msg: Message):
    if msg.chat.type == ChatType.PRIVATE and msg.from_user:
        await add_user(msg.from_user.id)
        try:
            await Safegram.send_message(
                LOGGER_ID,
                f"👤 **New User Started Bot**\n\n🆔: `{msg.from_user.id}`\n👤: [{msg.from_user.first_name}](tg://user?id={msg.from_user.id})",
                parse_mode=ParseMode.MARKDOWN,
            )
        except Exception:
            pass

    try:
        await msg.reply_photo(
            photo="https://files.catbox.moe/httj0w.jpg",
            caption=START_TEXT,
            reply_markup=get_main_buttons(),
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        await msg.reply_text(START_TEXT, reply_markup=get_main_buttons(), parse_mode=ParseMode.HTML)

@Safegram.on_callback_query(filters.regex("show_help"))
async def help_panel(_, query: CallbackQuery):
    await query.message.edit_text(
        HELP_TEXT,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("◀️ ʙᴀᴄᴋ", callback_data="back_to_start")],
        ]),
        parse_mode=ParseMode.HTML,
    )

@Safegram.on_callback_query(filters.regex("back_to_start"))
async def back_to_start(_, query: CallbackQuery):
    await query.message.edit_text(
        START_TEXT,
        reply_markup=get_main_buttons(),
        parse_mode=ParseMode.HTML,
    )

@Safegram.on_message(filters.command("ping"))
async def ping_command(_, message: Message):
    uptime = time_formatter((time.time() - start_time) * 1000)
    cpu = psutil.cpu_percent()
    disk = psutil.disk_usage("/")
    python_version = platform.python_version()

    try:
        await message.reply_photo(
            photo="https://files.catbox.moe/httj0w.jpg",
            caption=(
                f"🏓 **ᴘᴏɴɢ ʀᴇꜱᴘᴏɴꜱᴇ!**\n\n"
                f"➪ ᴜᴘᴛɪᴍᴇ: `{uptime}`\n"
                f"➪ ᴄᴘᴜ: `{cpu}%`\n"
                f"➪ ᴅɪꜱᴋ: `{size_formatter(disk.used)} / {size_formatter(disk.total)}`\n"
                f"➪ ꜰʀᴇᴇ: `{size_formatter(disk.free)}`\n"
                f"➪ ᴘʏᴛʜᴏɴ: `{python_version}`"
            ),
            reply_markup=get_ping_stats_buttons(),
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        await message.reply_text(
            f"🏓 **ᴘᴏɴɢ ʀᴇꜱᴘᴏɴꜱᴇ!**\n\n"
            f"➪ ᴜᴘᴛɪᴍᴇ: `{uptime}`\n"
            f"➪ ᴄᴘᴜ: `{cpu}%`\n"
            f"➪ ᴅɪꜱᴋ: `{size_formatter(disk.used)} / {size_formatter(disk.total)}`\n"
            f"➪ ꜰʀᴇᴇ: `{size_formatter(disk.free)}`\n"
            f"➪ ᴘʏᴛʜᴏɴ: `{python_version}`",
            reply_markup=get_ping_stats_buttons(),
            parse_mode=ParseMode.MARKDOWN,
        )

@Safegram.on_message(filters.command("stats"))
async def stats_command(_, message: Message):
    users = await get_all_users()
    chats = await get_all_chats()
    uptime = time_formatter((time.time() - start_time) * 1000)
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    try:
        await message.reply_photo(
            photo="https://files.catbox.moe/httj0w.jpg",
            caption=(
                f"📊 **ʙᴏᴛ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ**\n\n"
                f"👥 ᴜꜱᴇʀꜱ: `{len(users)}`\n"
                f"👨‍👩‍👧‍👦 ɢʀᴏᴜᴘꜱ: `{len(chats)}`\n"
                f"⏱️ ᴜᴘᴛɪᴍᴇ: `{uptime}`\n\n"
                f"🧠 ᴄᴘᴜ: `{cpu}%`\n"
                f"💾 ʀᴀᴍ: `{ram.percent}%`\n"
                f"🗃️ ᴅɪꜱᴋ: `{size_formatter(disk.used)} / {size_formatter(disk.total)}`\n"
                f"📂 ꜰʀᴇᴇ: `{size_formatter(disk.free)}`"
            ),
            reply_markup=get_ping_stats_buttons(),
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        await message.reply_text(
            f"📊 **ʙᴏᴛ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ**\n\n"
            f"👥 ᴜꜱᴇʀꜱ: `{len(users)}`\n"
            f"👨‍👩‍👧‍👦 ɢʀᴏᴜᴘꜱ: `{len(chats)}`\n"
            f"⏱️ ᴜᴘᴛɪᴍᴇ: `{uptime}`\n\n"
            f"🧠 ᴄᴘᴜ: `{cpu}%`\n"
            f"💾 ʀᴀᴍ: `{ram.percent}%`\n"
            f"🗃️ ᴅɪꜱᴋ: `{size_formatter(disk.used)} / {size_formatter(disk.total)}`\n"
            f"📂 ꜰʀᴇᴇ: `{size_formatter(disk.free)}`",
            reply_markup=get_ping_stats_buttons(),
            parse_mode=ParseMode.MARKDOWN,
        )
