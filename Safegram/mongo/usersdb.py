from Safegram.mongo.mongo import db

users_col = db.users

async def add_user(user_id: int) -> None:
    await users_col.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True,
    )

async def remove_user(user_id: int) -> None:
    await users_col.delete_one({"user_id": user_id})

async def get_all_users() -> list[int]:
    cursor = users_col.find({}, {"user_id": 1})
    return [doc["user_id"] async for doc in cursor]
