import os
from dotenv import load_dotenv

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
API_ID = 25855080
API_HASH = "5727997f0ecf9cee66b3e9b107a5dcca"
BOT_TOKEN = "8389067983:AAFF0Wunfqttw5UZly_1_MW-Js-K4fM-kSc"
# Bot configuration
OWNER_ID = 6375272628
LOGGER_ID = -1002361519040
MONGO_URL = "mongodb+srv://Mangokimkc:Mangokimkc@cluster0.owifdsg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
