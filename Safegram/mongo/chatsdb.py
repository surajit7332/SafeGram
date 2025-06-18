from Safegram.mongo.mongo import db

chats_col = db.chats

async def add_chat(chat_id: int) -> None:
    await chats_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id}},
        upsert=True,
    )

async def remove_chat(chat_id: int) -> None:
    await chats_col.delete_one({"chat_id": chat_id})

async def get_all_chats() -> list[int]:
    cursor = chats_col.find({}, {"chat_id": 1})
    return [doc["chat_id"] async for doc in cursor]
