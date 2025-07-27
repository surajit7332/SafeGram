from __future__ import annotations

from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatMemberUpdated

from config import LOGGER_ID
from Safegram import Safegram
from Safegram.mongo.chatsdb import add_chat, remove_chat

@Safegram.on_chat_member_updated()
async def bot_membership_watcher(_, update: ChatMemberUpdated) -> None:
    member = None
    if update.new_chat_member and update.new_chat_member.user and update.new_chat_member.user.is_self:
        member = update.new_chat_member
    elif update.old_chat_member and update.old_chat_member.user and update.old_chat_member.user.is_self:
        member = update.old_chat_member

    if member is None:
        return

    chat = update.chat
    chat_id = chat.id
    status = member.status

    if status in {
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    }:
        await add_chat(chat_id)
        try:
            await Safegram.send_message(
                LOGGER_ID,
                f"✅ **Bot Added To Group**\n\n📌 `{chat.title}`\n🆔 `{chat_id}`",
            )
        except Exception:
            pass

        
    elif status in {ChatMemberStatus.LEFT, ChatMemberStatus.KICKED}:
        await remove_chat(chat_id)
        try:
            await Safegram.send_message(
                LOGGER_ID,
                f"❌ **Bot Removed From Group**\n\n📌 `{chat.title}`\n🆔 `{chat_id}`",
            )
        except Exception:
            pass
