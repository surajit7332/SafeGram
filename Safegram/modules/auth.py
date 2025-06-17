import os
import json
from pyrogram import filters
from pyrogram.types import Message
from config import OWNER_ID
from Safegram import Safegram

AUTHORIZED_USERS_FILE = "authorized_users.json"
AUTHORIZED_USERS = []

def load_authorized_users():
    if os.path.exists(AUTHORIZED_USERS_FILE):
        with open(AUTHORIZED_USERS_FILE, "r") as f:
            return json.load(f)
    return [OWNER_ID]

def save_authorized_users(users):
    with open(AUTHORIZED_USERS_FILE, "w") as f:
        json.dump(users, f)

AUTHORIZED_USERS = load_authorized_users()

@Safegram.on_message(filters.command("auth") & filters.user(OWNER_ID))
async def auth_user(_, message: Message):
    if len(message.command) != 2 or not message.command[1].isdigit():
        return await message.reply_text("⚠️ **ᴜsᴀɢᴇ:** `/auth <user_id>`", quote=True)

    user_id = int(message.command[1])
    if user_id in AUTHORIZED_USERS:
        await message.reply_text(f"👤 **{user_id} ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ.**", quote=True)
    else:
        AUTHORIZED_USERS.append(user_id)
        save_authorized_users(AUTHORIZED_USERS)
        await message.reply_text(f"✅ **{user_id} ʜᴀs ʙᴇᴇɴ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ.**", quote=True)

@Safegram.on_message(filters.command("unauth") & filters.user(OWNER_ID))
async def unauth_user(_, message: Message):
    if len(message.command) != 2 or not message.command[1].isdigit():
        return await message.reply_text("⚠️ **ᴜsᴀɢᴇ:** `/unauth <user_id>`", quote=True)

    user_id = int(message.command[1])
    if user_id in AUTHORIZED_USERS:
        AUTHORIZED_USERS.remove(user_id)
        save_authorized_users(AUTHORIZED_USERS)
        await message.reply_text(f"🚫 **{user_id} ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ᴛʀᴏᴍ ᴀᴜᴛʜ ʟɪsᴛ.**", quote=True)
    else:
        await message.reply_text(f"❌ **{user_id} ɪs ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ.**", quote=True)

@Safegram.on_message(filters.command("listauth") & filters.user(OWNER_ID))
async def list_authorized_users(_, message: Message):
    if not AUTHORIZED_USERS:
        return await message.reply_text("📭 **ɴᴏ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs ꜰᴏᴜɴᴅ.**", quote=True)

    auth_list = "\n".join([f"• `{uid}`" for uid in AUTHORIZED_USERS])
    await message.reply_text(
        f"📋 **ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs:**\n\n{auth_list}", quote=True
    )
