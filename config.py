import os
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

def get_env_variable(name: str, required: bool = True, cast_func=None):
    value = os.getenv(name)

    if value is None:
        if required:
            raise EnvironmentError(f"Required environment variable '{name}' not set.")
        return None

    if cast_func:
        try:
            return cast_func(value)
        except ValueError:
            raise ValueError(f"Environment variable '{name}' could not be casted using {cast_func.__name__}.")

    return value

# Telegram API credentials
API_ID = get_env_variable("API_ID", cast_func=int)
API_HASH = get_env_variable("API_HASH")
BOT_TOKEN = get_env_variable("BOT_TOKEN")

# Bot configuration
OWNER_ID = get_env_variable("OWNER_ID", cast_func=int)
LOGGER_ID = get_env_variable("LOGGER_ID", cast_func=int)
MONGO_URL = get_env_variable("MONGO_URL")
