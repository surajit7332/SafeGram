from pyrogram import filters
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.types import Message
from config import OWNER_ID
from Safegram import Safegram
from Safegram.mongo.authdb import (
    add_authorized_user,
    remove_authorized_user,
    get_authorized_users,
)

async def is_privileged_user(message: Message) -> bool:
    if message.from_user.id == OWNER_ID:
        return True
    member = await Safegram.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)

@Safegram.on_message(filters.command("auth") & filters.group)
async def auth_user(_, message: Message):
    if not (await is_privileged_user(message)):
        return

    if len(message.command) != 2 or not message.command[1].isdigit():
        return await message.reply_text(
            "⚠️ ᴜꜱᴀɢᴇ: `/auth <user_id>`",
            parse_mode=ParseMode.MARKDOWN
        )

    user_id = int(message.command[1])
    await add_authorized_user(message.chat.id, user_id)
    await message.reply_text(
        f"✅ `{user_id}` ʜᴀꜱ ʙᴇᴇɴ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ.",
        parse_mode=ParseMode.MARKDOWN
    )

@Safegram.on_message(filters.command("unauth") & filters.group)
async def unauth_user(_, message: Message):
    if not (await is_privileged_user(message)):
        return

    if len(message.command) != 2 or not message.command[1].isdigit():
        return await message.reply_text(
            "⚠️ ᴜꜱᴀɢᴇ: `/unauth <user_id>`",
            parse_mode=ParseMode.MARKDOWN
        )

    user_id = int(message.command[1])
    await remove_authorized_user(message.chat.id, user_id)
    await message.reply_text(
        f"🚫 `{user_id}` ʜᴀꜱ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ᴀᴜᴛʜ ʟɪꜱᴛ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ.",
        parse_mode=ParseMode.MARKDOWN
    )

@Safegram.on_message(filters.command("listauth") & filters.group)
async def list_authorized_users(_, message: Message):
    if not (await is_privileged_user(message)):
        return

    authorized = await get_authorized_users(message.chat.id)
    if not authorized:
        return await message.reply_text(
            "📭 ɴᴏ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜꜱᴇʀꜱ ꜰᴏᴜɴᴅ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ.",
            parse_mode=ParseMode.MARKDOWN
        )

    user_list = "\n".join([f"• `{uid}`" for uid in authorized])
    chat_name = message.chat.title or "ᴜɴɴᴀᴍᴇᴅ"
    chat_id = message.chat.id

    formatted_msg = (
        f"📋 *ᴀᴜᴛʜ ʟɪꜱᴛ ᴘᴀɴᴇʟ*\n\n"
        f"*ᴄʜᴀᴛ:* {chat_name}\n"
        f"*ɪᴅ:* `{chat_id}`\n\n"
        f"*ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜꜱᴇʀꜱ:*\n{user_list}"
    )

    await message.reply_text(formatted_msg, parse_mode=ParseMode.MARKDOWN)
