from __future__ import annotations

from asyncio import sleep
from pyrogram import filters
from pyrogram.errors import FloodWait, PeerIdInvalid
from pyrogram.types import Message

from config import OWNER_ID
from Safegram import Safegram
from Safegram.mongo.usersdb import get_all_users
from Safegram.mongo.chatsdb import get_all_chats

async def send_broadcast(target, message: Message, payload_text: str):
    try:
        if message.reply_to_message:
            # Send media if present, else send text
            if message.reply_to_message.media:
                await message.reply_to_message.copy(target)
            elif payload_text:
                await Safegram.send_message(target, payload_text)
        else:
            await Safegram.send_message(target, payload_text)
        return True
    except FloodWait as e:
        await sleep(e.value)
        return await send_broadcast(target, message, payload_text)  # retry after wait
    except (PeerIdInvalid, Exception):
        return False

@Safegram.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_handler(_, message: Message):
    """
    Usage:
    /broadcast [-user] [-group] <message>
    Reply to a message (media/text) + /broadcast to send media/text.
    By default, it sends to all users and groups unless a flag is specified.
    """
    if len(message.command) == 1 and not message.reply_to_message:
        return await message.reply_text(
            "⚠️ Usage:\n`/broadcast [-user] [-group] <message>`\n"
            "Or reply to a media/text message with `/broadcast`",
            quote=True
        )

    # Parse flags
    user_mode = "-user" in message.text
    group_mode = "-group" in message.text

    # Get payload
    payload = None
    if len(message.command) > 1:
        payload = message.text.split(None, 1)[1]
        for flag in ["-user", "-group"]:
            payload = payload.replace(flag, "")
        payload = payload.strip()

    if payload is None and message.reply_to_message:
        payload = message.reply_to_message.text or message.reply_to_message.caption

    if not payload and not message.reply_to_message:
        return await message.reply_text("❌ Nothing to broadcast.", quote=True)

    # Get targets
    targets = []
    if user_mode:
        targets.extend(await get_all_users())
    if group_mode:
        targets.extend(await get_all_chats())
    if not user_mode and not group_mode:
        # Default: all users and all chats
        targets = list(set(await get_all_users() + await get_all_chats()))

    sent = failed = 0

    for idx, target in enumerate(targets, 1):
        success = await send_broadcast(target, message, payload)
        if success:
            sent += 1
        else:
            failed += 1
        await sleep(0.05)
        if idx % 50 == 0:
            await message.reply_text(f"📣 Progress: Sent: `{sent}` | Failed: `{failed}`")

    await message.reply_text(
        f"📣 Broadcast completed\n\n✅ Sent: `{sent}`\n❌ Failed: `{failed}`",
        quote=True,
    )
