from __future__ import annotations

import random
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.types import ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import LOGGER_ID
from Safegram import Safegram
from Safegram.mongo.chatsdb import add_chat, remove_chat

photo = [
    "https://telegra.ph/file/1949480f01355b4e87d26.jpg",
    "https://telegra.ph/file/3ef2cc0ad2bc548bafb30.jpg",
    "https://telegra.ph/file/a7d663cd2de689b811729.jpg",
    "https://telegra.ph/file/6f19dc23847f5b005e922.jpg",
    "https://telegra.ph/file/2973150dd62fd27a3a6ba.jpg",
]

# Handles when Safegram joins a new chat
async def on_my_join(client: Safegram, chat: "pyrogram.types.Chat", added_by: "pyrogram.types.User"):
    link = await client.export_chat_invite_link(chat.id)
    count = await client.get_chat_members_count(chat.id)
    msg = (
        f"📝 ʙᴏᴛ ᴀᴅᴅᴇᴅ ɪɴ ᴀ ɴᴇᴡ ɢʀᴏᴜᴘ\n\n"
        f"____________________________________\n\n"
        f"📌 ᴄʜᴀᴛ ɴᴀᴍᴇ: {chat.title}\n"
        f"🍂 ᴄʜᴀᴛ ɪᴅ: {chat.id}\n"
        f"🔐 ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ: @{chat.username if chat.username else 'N/A'}\n"
        f"🛰 ᴄʜᴀᴛ ʟɪɴᴋ: [ᴄʟɪᴄᴋ]({link})\n"
        f"📈 ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs: {count}\n"
        f"🤔 ᴀᴅᴅᴇᴅ ʙʏ: {added_by.mention if added_by else 'Unknown'}"
    )
    await client.send_photo(
        LOGGER_ID,
        photo=random.choice(photo),
        caption=msg,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("sᴇᴇ ɢʀᴏᴜᴘ👀", url=link)]]),
        parse_mode=ParseMode.HTML,
    )
    await add_chat(chat.id)

# Handles when Safegram leaves a chat
async def on_my_leave(client: Safegram, chat: "pyrogram.types.Chat", removed_by: "pyrogram.types.User"):
    left = (
        f"✫ <b><u>#𝐋ᴇғᴛ_𝐆ʀᴏᴜᴘ</u></b> ✫\n\n"
        f"𝐂ʜᴀᴛ 𝐓ɪᴛʟᴇ : {chat.title}\n\n"
        f"𝐂ʜᴀᴛ 𝐈ᴅ : {chat.id}\n\n"
        f"𝐑ᴇᴍᴏᴠᴇᴅ 𝐁ʏ : {removed_by.mention if removed_by else 'Unknown'}\n\n"
        f"𝐁ᴏᴛ : @{client.me.username}"
    )
    await client.send_photo(
        LOGGER_ID,
        photo=random.choice(photo),
        caption=left,
        parse_mode=ParseMode.HTML
    )
    await remove_chat(chat.id)

# Watch for chat member updates to trigger join/leave events
@Safegram.on_chat_member_updated()
async def watcher(client: Safegram, update: ChatMemberUpdated):
    # Bot joined the chat
    if (
        update.new_chat_member.user.id == client.me.id
        and update.old_chat_member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
        and update.new_chat_member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    ):
        await on_my_join(client, update.chat, update.from_user)
    # Bot left the chat
    elif (
        update.old_chat_member.user.id == client.me.id
        and update.old_chat_member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
        and update.new_chat_member.status == ChatMemberStatus.LEFT
    ):
        await on_my_leave(client, update.chat, update.from_user)


