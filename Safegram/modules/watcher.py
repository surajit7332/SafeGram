from pyrogram.types import ChatMemberUpdated
from config import LOGGER_ID
from Safegram import Safegram
from Safegram.mongo.chatsdb import add_chat, remove_chat

@Safegram.on_chat_member_updated()
async def handle_bot_group_events(_, update: ChatMemberUpdated):
    if not update.new_chat_member.user.is_self:
        return

    chat = update.chat
    chat_id = chat.id

    if update.new_chat_member.status in ("member", "administrator"):
        await add_chat(chat_id)
        try:
            await Safegram.send_message(
                LOGGER_ID,
                f"✅ **Bot Added To Group**\n\n📌 `{chat.title}`\n🆔 `{chat.id}`"
            )
        except:
            pass

    elif update.new_chat_member.status in ("kicked", "left"):
        await remove_chat(chat_id)
        try:
            await Safegram.send_message(
                LOGGER_ID,
                f"❌ **Bot Removed From Group**\n\n📌 `{chat.title}`\n🆔 `{chat.id}`"
            )
        except:
            pass


@Safegram.on_chat_member_updated()
async def auto_leave_if_no_admin(_, update: ChatMemberUpdated):
    if not update.new_chat_member.user.is_self:
        return

    chat = update.chat
    chat_id = chat.id

    if update.new_chat_member.status == "member":
        try:
            await Safegram.send_message(
                chat_id,
                "**🚫 ɪ ɴᴇᴇᴅ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴡᴏʀᴋ. ʟᴇᴀᴠɪɴɢ ᴛʜɪs ɢʀᴏᴜᴘ.**"
            )
            await Safegram.leave_chat(chat_id)
        except Exception:
            pass
