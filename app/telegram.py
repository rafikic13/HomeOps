from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from app.config import (
    TELEGRAM_ALLOWED_CHAT_ID,
    TELEGRAM_BOT_TOKEN,
    validate_telegram_config,
)
from app.prometheus import get_target_statuses


def is_authorized(update: Update) -> bool:
    if update.effective_chat is None:
        return False

    return update.effective_chat.id == int(TELEGRAM_ALLOWED_CHAT_ID)


async def status_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if not is_authorized(update):
        if update.message:
            await update.message.reply_text("Unauthorized.")
        return

    try:
        targets = get_target_statuses()

        lines = ["HomeOps infrastructure status:"]

        for target in targets:
            lines.append(
                f"- {target['job']}: {target['status']} "
                f"({target['instance']})"
            )

        message = "\n".join(lines)

    except RuntimeError as error:
        message = f"Status check failed: {error}"

    if update.message:
        await update.message.reply_text(message)


def run_bot() -> None:
    validate_telegram_config()

    application = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("status", status_command)
    )

    print("HomeOps Telegram bot is running.")
    application.run_polling()


if __name__ == "__main__":
    run_bot()
