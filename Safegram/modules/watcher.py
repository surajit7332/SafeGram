import logging
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter
from pyrogram.types import ChatMemberUpdated

from config import LOGGER_ID
from Safegram import Safegram
from Safegram.mongo.chatsdb import add_chat, remove_chat

logger = logging.getLogger(__name__)

@Safegram.on_chat_member_updated()
async def bot_membership_watcher(_, update: ChatMemberUpdated) -> None:
    logger.info(f"Received chat_member_updated: {update}")

    member = None
    if update.new_chat_member and update.new_chat_member.user and update.new_chat_member.user.is_self:
        member = update.new_chat_member
        actor = update.from_user
        action = "Added"
        logger.info(f"Bot added to group {update.chat.id} by {actor.username if actor else 'Unknown'}")
    elif update.old_chat_member and update.old_chat_member.user and update.old_chat_member.user.is_self:
        member = update.old_chat_member
        actor = update.from_user
        action = "Removed"
        logger.info(f"Bot removed from group {update.chat.id} by {actor.username if actor else 'Unknown'}")
    else:
        logger.debug("No bot membership change detected in update.")
        return

    chat = update.chat
    chat_id = chat.id
    status = member.status

    chat_username = chat.username if chat.username else "private"
    actor_username = actor.username if actor and actor.username else (actor.first_name if actor else "Unknown")

    # Get list of admin members only if bot is ADDED
    members_list = None
    if status in {
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    }:
        try:
            members = []
            async for m in Safegram.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
                name = m.user.username or m.user.first_name or "Unknown"
                members.append(name)
            members_list = ', '.join(members)
            logger.info(f"Fetched admin members for chat {chat_id}: {members_list}")
        except Exception as e:
            members_list = f"Unable to fetch members: {e}"
            logger.error(f"Error fetching admin members for chat {chat_id}: {e}")

        await add_chat(chat_id)
        try:
            await Safegram.send_message(
                LOGGER_ID,
                f"✅ **Bot Added To Group**\n\n"
                f"📌 Title: `{chat.title}`\n"
                f"🆔 ID: `{chat_id}`\n"
                f"🔗 Username: `{chat_username}`\n"
                f"👤 Added by: `{actor_username}`\n"
                f"👥 Admins: {members_list}",
            )
            logger.info(f"Bot added message sent for chat {chat_id}")
        except Exception as e:
            logger.error(f"Error sending add message for chat {chat_id}: {e}")

    elif status in {ChatMemberStatus.LEFT, ChatMemberStatus.KICKED}:
        members_list = "Unavailable (bot removed)"
        await remove_chat(chat_id)
        try:
            await Safegram.send_message(
                LOGGER_ID,
                f"❌ **Bot Removed From Group**\n\n"
                f"📌 Title: `{chat.title}`\n"
                f"🆔 ID: `{chat_id}`\n"
                f"🔗 Username: `{chat_username}`\n"
                f"👤 Removed by: `{actor_username}`\n"
                f"👥 Admins: {members_list}",
            )
            logger.info(f"Bot removed message sent for chat {chat_id}")
        except Exception as e:
            logger.error(f"Error sending remove message for chat {chat_id}: {e}")
