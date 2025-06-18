from __future__ import annotations

from typing import Optional

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message, User

from config import OWNER_ID
from Safegram import Safegram
from Safegram.mongo.authdb import (
    add_authorized_user,
    remove_authorized_user,
    get_authorized_users,
)

async def _is_privileged_user(message: Message) -> bool:
    if message.from_user and message.from_user.id == OWNER_ID:
        return True
    member = await Safegram.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)

async def _resolve_user(identifier: str) -> Optional[int]:
    if identifier.isdigit():
        return int(identifier)
    username = identifier.lstrip("@")
    try:
        user: User = await Safegram.get_users(username)
        return user.id
    except Exception:
        return None

def _usage(cmd: str) -> str:
    return f"⚠️ Usage:\n`/{cmd} user_id | @username` –or– reply to the user’s message"

async def _extract_target_user_id(message: Message) -> Optional[int]:
    if message.reply_to_message and len(message.command) == 1:
        return message.reply_to_message.from_user.id
    if len(message.command) >= 2:
        return await _resolve_user(message.command[1])
    return None

async def _send_usage(message: Message, cmd: str) -> None:
    await message.reply_text(_usage(cmd), quote=True)

@Safegram.on_message(filters.command("auth") & filters.group)
async def auth_user(_, message: Message) -> None:
    if not await _is_privileged_user(message):
        return
    user_id = await _extract_target_user_id(message)
    if user_id is None:
        return await _send_usage(message, "auth")
    await add_authorized_user(message.chat.id, user_id)
    await message.reply_text(
        f"✅ [User](tg://user?id={user_id}) has been authorised in this chat.",
        quote=True,
    )

@Safegram.on_message(filters.command("unauth") & filters.group)
async def unauth_user(_, message: Message) -> None:
    if not await _is_privileged_user(message):
        return
    user_id = await _extract_target_user_id(message)
    if user_id is None:
        return await _send_usage(message, "unauth")
    await remove_authorized_user(message.chat.id, user_id)
    await message.reply_text(
        f"🚫 [User](tg://user?id={user_id}) has been removed from the auth list.",
        quote=True,
    )

@Safegram.on_message(filters.command("listauth") & filters.group)
async def list_authorized_users(_, message: Message) -> None:
    if not await _is_privileged_user(message):
        return
    authorised_user_ids = await get_authorized_users(message.chat.id)
    if not authorised_user_ids:
        return await message.reply_text("📭 No authorised users found in this chat.")
    mentions = "\n".join(f"• [User](tg://user?id={uid}) " for uid in authorised_user_ids)
    reply = (
        "📋 **Auth List Panel**\n\n"
        f"**Chat:** {message.chat.title or 'Unnamed Chat'}\n"
        f"**ID:** `{message.chat.id}`\n\n"
        f"**Authorised Users:**\n{mentions}"
    )
    await message.reply_text(reply, quote=True, disable_web_page_preview=True)
