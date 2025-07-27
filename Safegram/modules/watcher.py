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
        actor = update.from_user  # User who added the bot
        action = "Added"
    elif update.old_chat_member and update.old_chat_member.user and update.old_chat_member.user.is_self:
        member = update.old_chat_member
        actor = update.from_user  # User who removed the bot
        action = "Removed"
    else:
        return

    chat = update.chat
    chat_id = chat.id
    status = member.status

    # Get chat username or 'private'
    chat_username = chat.username if chat.username else "private"

    # Get actor username or name
    actor_username = actor.username if actor and actor.username else (actor.first_name if actor else "Unknown")

    # Get chat members (fetching only admins due to Telegram restrictions)
    try:
        members = []
        async for m in Safegram.get_chat_members(chat_id, filter="administrators"):
            user = m.user
            members.append(user.username if user.username else user.first_name)
        members_list = ', '.join(members)
    except Exception:
        members_list = "Unable to fetch members"

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
                f"👤 Added by: `{actor_username}`\n"
                f"👥 Members: {members_list}",
            )
        except Exception:
            pass

        # REMOVED: auto-leave logic if bot is not admin
        # (No code for bot to leave if not admin)

    elif status in {ChatMemberStatus.LEFT, ChatMemberStatus.KICKED}:
        await remove_chat(chat_id)
        try:
            await Safegram.send_message(
                LOGGER_ID,
                f"❌ **Bot Removed From Group**\n\n"
                f"📌 Title: `{chat.title}`\n"
                f"🆔 ID: `{chat_id}`\n"
                f"🔗 Username: `{chat_username}`\n"
                f"👤 Removed by: `{actor_username}`\n"
                f"👥 Members: {members_list}",
            )
        except Exception:
            pass
