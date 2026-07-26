import os

from dotenv import load_dotenv


load_dotenv(override=True)


PROMETHEUS_URL = os.getenv(
    "PROMETHEUS_URL",
    "http://localhost:9090",
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_ALLOWED_CHAT_ID = os.getenv("TELEGRAM_ALLOWED_CHAT_ID")


def validate_telegram_config() -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is missing from the environment."
        )

    if not TELEGRAM_ALLOWED_CHAT_ID:
        raise RuntimeError(
            "TELEGRAM_ALLOWED_CHAT_ID is missing from the environment."
        )

    try:
        int(TELEGRAM_ALLOWED_CHAT_ID)

    except ValueError as error:
        raise RuntimeError(
            "TELEGRAM_ALLOWED_CHAT_ID must be an integer."
        ) from error
