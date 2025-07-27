from __future__ import annotations

from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatMemberUpdated

from config import LOGGER_ID
from Safegram import Safegram
from Safegram.mongo.chatsdb import add_chat, remove_chat

