from __future__ import annotations

from asyncio import sleep

from pyrogram import filters
from pyrogram.errors import FloodWait, PeerIdInvalid
from pyrogram.types import Message

from config import OWNER_ID, LOG_GROUP_ID
from Safegram import Safegram
from Safegram.mongo.usersdb import get_all_users
from Safegram.mongo.chatsdb import get_all_chats

@Safegram.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_handler(_, message: Message):
    # Usage message
    if len(message.command) == 1 and not message.reply_to_message:
        return await message.reply_text(
            "⚠️ Usage: `/broadcast [-user|-chat] [-pin] [-forward] <message>`\n"
            "Reply to a message to forward/broadcast it.",
            quote=True
        )

    # Flag parsing
    user_mode = chat_mode = pin_mode = False
    forward_only = False
    payload = None

    args = message.text.split()[1:] if len(message.command) > 1 else []
    # Parse flags
    if "-user" in args:
        user_mode = True
        args.remove("-user")
    if "-chat" in args:
        chat_mode = True
        args.remove("-chat")
    if "-pin" in args:
        pin_mode = True
        args.remove("-pin")
    if "-forward" in args:
        forward_only = True
        args.remove("-forward")

    # If neither mode specified, do both
    if not user_mode and not chat_mode:
        user_mode = chat_mode = True

    # Get payload
    payload = " ".join(args) if args else None

    is_forward = False
    if message.reply_to_message:
        if forward_only:
            payload = None
            is_forward = True
        else:
            if not payload:
                payload = message.reply_to_message.text or message.reply_to_message.caption
            is_forward = True

    if not payload and not (message.reply_to_message and is_forward):
        return await message.reply_text("❌ Nothing to broadcast.", quote=True)

    sent = failed = pinned = 0

    # Gather targets
    targets = []
    if user_mode:
        targets += await get_all_users()
    if chat_mode:
        targets += await get_all_chats()

    targets = list(set(targets))  # Remove duplicates

    for target in targets:
        try:
            if is_forward:
                sent_msg = await Safegram.forward_messages(
                    target,
                    from_chat_id=message.reply_to_message.chat.id,
                    message_id=message.reply_to_message.message_id
                )
            else:
                sent_msg = await Safegram.send_message(
                    target,
                    payload,
                )
            sent += 1

            # Pin if requested and target is a chat
            if pin_mode and target in await get_all_chats():
                try:
                    await Safegram.pin_chat_message(target, sent_msg.id)
                    pinned += 1
                except Exception:
                    pass

            await sleep(0.05)
        except FloodWait as e:
            await sleep(e.value)
        except (PeerIdInvalid, Exception):
            failed += 1

    # Banner message for log group
    banner_msg = (
        "✅ **Broadcast Completed**\n"
        f"👤 By: [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
        f"📩 Type: {'Forward' if is_forward else 'Text'}\n"
        f"🔈 Sent: `{sent}`\n"
        f"📌 Pinned: `{pinned}`\n"
        f"❌ Failed: `{failed}`\n"
        f"📝 Message: {payload or (message.reply_to_message.text if message.reply_to_message else '')[:100]}"
    )
    try:
        await Safegram.send_message(LOG_GROUP_ID, banner_msg, disable_web_page_preview=True)
    except Exception:
        pass

    await message.reply_text(
        f"📣 Broadcast completed\n\n✅ Sent: `{sent}`\n📌 Pinned: `{pinned}`\n❌ Failed: `{failed}`",
        quote=True,
    )
