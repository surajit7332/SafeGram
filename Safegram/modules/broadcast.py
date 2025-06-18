from __future__ import annotations

from asyncio import sleep

from pyrogram import filters
from pyrogram.errors import FloodWait, PeerIdInvalid
from pyrogram.types import Message

from config import OWNER_ID
from Safegram import Safegram
from Safegram.mongo.usersdb import get_all_users
from Safegram.mongo.chatsdb import get_all_chats

@Safegram.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_handler(_, message: Message):
    if len(message.command) == 1 and not message.reply_to_message:
        return await message.reply_text("⚠️ Usage: `/broadcast [-user] <message>`", quote=True)

    user_mode = False
    payload = None

    if len(message.command) > 1:
        payload = message.text.split(None, 1)[1]
        if payload.startswith("-user"):
            user_mode = True
            payload = payload.replace("-user", "", 1).strip()

    if payload is None and message.reply_to_message:
        payload = message.reply_to_message.text or message.reply_to_message.caption

    if not payload:
        return await message.reply_text("❌ Nothing to broadcast.", quote=True)

    targets = await get_all_users() if user_mode else await get_all_chats()
    sent = failed = 0

    for target in targets:
        try:
            await Safegram.send_message(target, payload)
            sent += 1
            await sleep(0.05)
        except FloodWait as e:
            await sleep(e.value)
        except (PeerIdInvalid, Exception):
            failed += 1

    await message.reply_text(
        f"📣 Broadcast completed\n\n✅ Sent: `{sent}`\n❌ Failed: `{failed}`",
        quote=True,
    )
