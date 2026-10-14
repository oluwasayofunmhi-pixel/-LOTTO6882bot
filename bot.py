import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
from moviepy.editor import VideoFileClip

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Convert Video", callback_data="convert")],
        [InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("About", callback_data="about")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to Video to GIF Converter.\n\n"
        "Send me a short video (under 20MB, under 30 seconds) "
        "and I will convert it into a GIF.",
        reply_markup=reply_markup,
    )


# ---------- /help ----------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "How to use this bot:\n\n"
        "1. Send or forward a short video (MP4 recommended).\n"
        "2. Wait a few seconds while it processes.\n"
        "3. Receive your GIF.\n\n"
        "Limits:\n"
        "- Max size: 20MB\n"
        "- Max length: 30 seconds\n\n"
        "Commands:\n"
        "/start - Main menu\n"
        "/help - This message\n"
        "/about - About this bot"
    )


# ---------- /about ----------
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Video to GIF Converter\n\n"
        "A simple tool that converts short videos into GIFs directly inside Telegram.\n\n"
        "No external app or website required."
    )


# ---------- Inline button handler ----------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "convert":
        await query.message.reply_text(
            "Send me a short video now (under 20MB, under 30 seconds)."
        )
    elif query.data == "help":
        await query.message.reply_text(
            "1. Send a short video.\n2. Wait for conversion.\n3. Receive your GIF."
        )
    elif query.data == "about":
        await query.message.reply_text(
            "Video to GIF Converter - convert short videos into GIFs inside Telegram."
        )


# ---------- Video handler ----------
async def convert_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video or update.message.document

    if not video:
        await update.message.reply_text("Please send a video file.")
        return

    # Size check (20MB limit)
    if video.file_size and video.file_size > 20 * 1024 * 1024:
        await update.message.reply_text(
            "Video is too large. Please send a video under 20MB."
        )
        return

    status_msg = await update.message.reply_text("Processing your video...")

    input_path = f"input_{update.message.message_id}.mp4"
    output_path = f"output_{update.message.message_id}.gif"

    try:
        file = await context.bot.get_file(video.file_id)
        await file.download_to_drive(input_path)

        clip = VideoFileClip(input_path)

        # Trim to max 30 seconds
        if clip.duration > 30:
            clip = clip.subclip(0, 30)

        # Resize for smaller GIF
        if clip.h > 320:
            clip = clip.resize(height=320)

        clip.write_gif(output_path, fps=10, program="ffmpeg", logger=None)
        clip.close()

        with open(output_path, "rb") as gif_file:
            await update.message.reply_animation(animation=gif_file)

        await status_msg.delete()

    except Exception as e:
        logging.error(f"Conversion error: {e}")
        await status_msg.edit_text(
            "Something went wrong. Try a shorter or smaller video."
        )
    finally:
        for f in [input_path, output_path]:
            if os.path.exists(f):
                os.remove(f)


# ---------- Main ----------
def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(
        MessageHandler(filters.VIDEO | filters.Document.VIDEO, convert_video)
    )

    logging.info("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
