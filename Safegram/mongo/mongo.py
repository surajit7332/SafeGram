import logging
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

logger = logging.getLogger(__name__)

try:
    mongo_client = AsyncIOMotorClient(MONGO_URL)
    db = mongo_client.safegram
    logger.info("✅ MongoDB connection established successfully.")
except Exception as e:
    logger.error(f"❌ Failed to connect to MongoDB: {e}")
    raise RuntimeError("MongoDB connection error")
