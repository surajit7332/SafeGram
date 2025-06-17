from pyrogram import filters
from pyrogram.errors import FloodWait, PeerIdInvalid
from pyrogram.types import Message
from asyncio import sleep
from config import OWNER_ID
from Safegram import Safegram
from Safegram.mongo.usersdb import get_all_users
from Safegram.mongo.chatsdb import get_all_chats


@Safegram.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ **ᴜsᴀɢᴇ:** `/broadcast [-user] message here`", quote=True)

    content = message.text.split(None, 1)[1]

    is_user_broadcast = False
    if content.startswith("-user"):
        is_user_broadcast = True
        content = content.replace("-user", "", 1).strip()

    sent = 0
    failed = 0

    targets = await get_all_users() if is_user_broadcast else await get_all_chats()

    for target_id in targets:
        try:
            await Safegram.send_message(target_id, content)
            sent += 1
            await sleep(0.1)
        except FloodWait as e:
            await sleep(e.value)
        except PeerIdInvalid:
            failed += 1
        except Exception:
            failed += 1

    await message.reply_text(
        f"📣 **ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ**\n\n"
        f"✅ ᴍᴇssᴀɢᴇ sᴇɴᴛ: `{sent}`\n"
        f"❌ ᴍᴇssᴀɢᴇ ꜰᴀɪʟᴇᴅ: `{failed}`",
        quote=True
    )
