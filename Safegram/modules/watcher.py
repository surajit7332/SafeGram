from __future__ import annotations

import logging
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatMemberUpdated

from config import LOGGER_ID
from Safegram import Safegram
from Safegram.mongo.chatsdb import add_chat, remove_chat

logger = logging.getLogger(__name__)

@Safegram.on_chat_member_updated()
async def bot_membership_watcher(_, update: ChatMemberUpdated) -> None:
    # Detect if the update involves the bot (new or old membership)
    member = None
    if update.new_chat_member and update.new_chat_member.user and update.new_chat_member.user.is_self:
        member = update.new_chat_member
    elif update.old_chat_member and update.old_chat_member.user and update.old_chat_member.user.is_self:
        member = update.old_chat_member

    if member is None:
        # Not related to the bot
        return

    chat = update.chat
    chat_id = chat.id
    status = member.status

    # Get actor username (who added/removed the bot)
    actor = update.from_user
    actor_username = (
        actor.username if actor and actor.username
        else (actor.first_name if actor else "Unknown")
    )

    chat_username = chat.username if chat.username else "private"

    # Bot added or promoted
    if status in {
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    }:
        await add_chat(chat_id)
        try:
            await Safegram.send_message(
                LOGGER_ID,
                f"✅ **Bot Added To Group**\n\n"
                f"📌 Title: `{chat.title}`\n"
                f"🆔 ID: `{chat_id}`\n"
                f"🔗 Username: `{chat_username}`\n"
                f"👤 Added by: `{actor_username}`",
            )
            logger.info(f"Bot added to group {chat_id} ({chat.title}) by {actor_username}")
        except Exception as e:
            logger.error(f"Failed to log bot addition for chat {chat_id}: {e}")

    # Bot removed, left, or banned
    elif status in {ChatMemberStatus.LEFT, ChatMemberStatus.BANNED}:
        await remove_chat(chat_id)
        try:
            await Safegram.send_message(
                LOGGER_ID,
                f"❌ **Bot Removed From Group**\n\n"
                f"📌 Title: `{chat.title}`\n"
                f"🆔 ID: `{chat_id}`\n"
                f"🔗 Username: `{chat_username}`\n"
                f"👤 Removed by: `{actor_username}`",
            )
            logger.info(f"Bot removed from group {chat_id} ({chat.title}) by {actor_username}")
        except Exception as e:
            logger.error(f"Failed to log bot removal for chat {chat_id}: {e}")
