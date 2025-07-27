import logging
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatMemberUpdated

from config import LOGGER_ID
from Safegram import Safegram
from Safegram.mongo.chatsdb import add_chat

logger = logging.getLogger(__name__)

@Safegram.on_chat_member_updated()
async def bot_membership_watcher(_, update: ChatMemberUpdated) -> None:
    logger.info(f"Received chat_member_updated: {update}")

    if update.new_chat_member and update.new_chat_member.user and update.new_chat_member.user.is_self:
        member = update.new_chat_member
        actor = update.from_user

        chat = update.chat
        chat_id = chat.id
        status = member.status

        chat_username = chat.username if chat.username else "private"
        actor_username = actor.username if actor and actor.username else (actor.first_name if actor else "Unknown")

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
                logger.info(f"Bot added message sent for chat {chat_id}")
            except Exception as e:
                logger.error(f"Error sending add message for chat {chat_id}: {e}")
    else:
        logger.debug("No bot added event detected in update.")
