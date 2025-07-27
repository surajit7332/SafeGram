import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Prince import app

# Chats currently being tagged
spam_chats = set()

# Inline buttons shown after tagging ends
END_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("💬 Support", url="https://t.me/YourSupportGroup"),
            InlineKeyboardButton("📢 Update", url="https://t.me/YourUpdateChannel"),
        ]
    ]
)


async def is_admin_or_owner(client, chat_id: int, user_id: int) -> bool:
    """Return True if the user is an admin or the owner of the chat."""
    try:
        member = await client.get_chat_member(chat_id, user_id)
    except UserNotParticipant:
        return False
    return member.status in {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER}


async def iter_members(chat_id, admins_only=False):
    """Yield chat members, skipping deleted accounts and bots."""
    async for member in app.get_chat_members(chat_id):
        user = member.user
        if user.is_deleted or user.is_bot:
            continue
        if admins_only:
            if member.status in {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER}:
                yield member
        else:
            yield member


async def do_tagging(chat_id, base_text, reply_to=None, admins_only=False):
    """Core logic to mention users in batches of 5 with delay."""
    spam_chats.add(chat_id)
    user_count = 0
    text_batch = ""

    async for member in iter_members(chat_id, admins_only=admins_only):
        if chat_id not in spam_chats:  # Stop if canceled
            break

        user_count += 1
        text_batch += f"<a href='tg://user?id={member.user.id}'>{member.user.first_name}</a>, "

        if user_count == 5:
            if reply_to:
                await reply_to.reply_text(f"{base_text}\n\n{text_batch}", disable_web_page_preview=True)
            else:
                await app.send_message(chat_id, f"{base_text}\n\n{text_batch}", disable_web_page_preview=True)

            await asyncio.sleep(2)
            user_count = 0
            text_batch = ""

    # Send any remaining mentions
    if chat_id in spam_chats and text_batch:
        if reply_to:
            await reply_to.reply_text(f"{base_text}\n\n{text_batch}", disable_web_page_preview=True)
        else:
            await app.send_message(chat_id, f"{base_text}\n\n{text_batch}", disable_web_page_preview=True)

    # Remove chat from spam_chats after completing
    if chat_id in spam_chats:
        spam_chats.discard(chat_id)
        await app.send_message(
            chat_id,
            "✅ Tagging process completed.",
            reply_markup=END_BUTTONS
        )


@app.on_message(filters.command(["tagall", "mention", "utag"]) & filters.group)
async def tag_all_users(client, message):
    """Tag all users in a group (admin-only)."""
    # Admin check
    if not await is_admin_or_owner(client, message.chat.id, message.from_user.id):
        return await message.reply_text("You must be an admin to use this command.")

    reply_to = message.reply_to_message
    # Message to send (default if no text provided)
    if len(message.command) > 1:
        base_text = message.text.split(None, 1)[1]
    elif reply_to:
        base_text = "Attention everyone!"
    else:
        return await message.reply_text("Reply to a message or provide text to tag everyone.")

    await do_tagging(message.chat.id, base_text, reply_to=reply_to, admins_only=False)


@app.on_message(filters.command(["tagadmins", "admintag"]) & filters.group)
async def tag_admins(client, message):
    """Tag only admins in a group (admin-only)."""
    # Admin check
    if not await is_admin_or_owner(client, message.chat.id, message.from_user.id):
        return await message.reply_text("You must be an admin to use this command.")

    reply_to = message.reply_to_message
    if len(message.command) > 1:
        base_text = message.text.split(None, 1)[1]
    elif reply_to:
        base_text = "Attention admins!"
    else:
        return await message.reply_text("Reply to a message or provide text to tag admins.")

    await do_tagging(message.chat.id, base_text, reply_to=reply_to, admins_only=True)


@app.on_message(filters.command(["cancel", "ustop"]) & filters.group)
async def cancel_tagging(client, message):
    """Cancel tagging for the current chat (only admins can do this)."""
    chat_id = message.chat.id
    if chat_id not in spam_chats:
        return await message.reply("Currently I'm not tagging anyone.")

    # Admin check
    if not await is_admin_or_owner(client, chat_id, message.from_user.id):
        return await message.reply_text("Only admins can stop the tagging.")

    spam_chats.discard(chat_id)
    return await message.reply(
        "🛑 Tagging process has been stopped.",
        reply_markup=END_BUTTONS
    )

