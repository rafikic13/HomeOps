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
from app.docker import (
    get_container_logs,
    get_container_statuses,
    restart_container,
)
from app.prometheus import get_target_statuses


MAX_TELEGRAM_MESSAGE_LENGTH = 4000


def is_authorized(update: Update) -> bool:
    if update.effective_chat is None:
        return False

    return update.effective_chat.id == int(
        TELEGRAM_ALLOWED_CHAT_ID
    )


async def reject_unauthorized(update: Update) -> None:
    if update.message:
        await update.message.reply_text("Unauthorized.")


async def status_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if not is_authorized(update):
        await reject_unauthorized(update)
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


async def containers_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if not is_authorized(update):
        await reject_unauthorized(update)
        return

    try:
        containers = get_container_statuses()
        lines = ["Docker containers:"]

        for container in containers:
            status_icon = (
                "✅"
                if container["status"] == "running"
                else "❌"
            )

            lines.append(
                f"{status_icon} {container['name']}: "
                f"{container['status']}"
            )

        message = "\n".join(lines)

    except RuntimeError as error:
        message = f"Container check failed: {error}"

    if update.message:
        await update.message.reply_text(message)


async def restart_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if not is_authorized(update):
        await reject_unauthorized(update)
        return

    if not context.args:
        if update.message:
            await update.message.reply_text(
                "Usage: /restart <container>"
            )
        return

    container_name = context.args[0]

    try:
        result = restart_container(container_name)
        message = f"✅ {result['message']}"

    except (ValueError, RuntimeError) as error:
        message = f"❌ {error}"

    if update.message:
        await update.message.reply_text(message)


async def logs_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if not is_authorized(update):
        await reject_unauthorized(update)
        return

    if not context.args:
        if update.message:
            await update.message.reply_text(
                "Usage: /logs <container> [lines]"
            )
        return

    container_name = context.args[0]
    tail = 10

    if len(context.args) >= 2:
        try:
            tail = int(context.args[1])

        except ValueError:
            if update.message:
                await update.message.reply_text(
                    "The number of log lines must be an integer."
                )
            return

    try:
        logs = get_container_logs(
            container_name,
            tail=tail,
        )

        message = (
            f"Recent logs for {container_name}:\n\n"
            f"{logs or 'No logs returned.'}"
        )

        if len(message) > MAX_TELEGRAM_MESSAGE_LENGTH:
            message = (
                message[:MAX_TELEGRAM_MESSAGE_LENGTH]
                + "\n\n[Output truncated]"
            )

    except (ValueError, RuntimeError) as error:
        message = f"❌ {error}"

    if update.message:
        await update.message.reply_text(message)


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if not is_authorized(update):
        await reject_unauthorized(update)
        return

    message = (
        "HomeOps commands:\n"
        "/status\n"
        "/containers\n"
        "/restart <container>\n"
        "/logs <container> [lines]\n"
        "/help"
    )

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
    application.add_handler(
        CommandHandler("containers", containers_command)
    )
    application.add_handler(
        CommandHandler("restart", restart_command)
    )
    application.add_handler(
        CommandHandler("logs", logs_command)
    )
    application.add_handler(
        CommandHandler("help", help_command)
    )

    print("HomeOps Telegram bot is running.")
    application.run_polling()


if __name__ == "__main__":
    run_bot()
