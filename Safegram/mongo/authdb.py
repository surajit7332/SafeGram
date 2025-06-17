from Safegram.mongo.mongo import db

auth_col = db.group_auth

async def add_authorized_user(chat_id: int, user_id: int) -> bool:
    return await auth_col.update_one(
        {"chat_id": chat_id},
        {"$addToSet": {"users": user_id}},
        upsert=True
    )

async def remove_authorized_user(chat_id: int, user_id: int) -> bool:
    return await auth_col.update_one(
        {"chat_id": chat_id},
        {"$pull": {"users": user_id}},
    )

async def get_authorized_users(chat_id: int) -> list[int]:
    data = await auth_col.find_one({"chat_id": chat_id})
    return data["users"] if data and "users" in data else []

async def is_user_authorized(chat_id: int, user_id: int) -> bool:
    data = await auth_col.find_one({"chat_id": chat_id})
    return bool(data and "users" in data and user_id in data["users"])
