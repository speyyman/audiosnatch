import subprocess
from pytube import YouTube
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update
import os
from dotenv import load_dotenv
load_dotenv()


TOKEN = os.environ.get("BOT_API_TOKEN")


async def download_and_convert(url, filename):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    downloaded_file = stream.download(filename='temp_video')

    mp3_filename = f"{filename}.mp3"
    subprocess.run([
        'ffmpeg', '-y',
        '-i', downloaded_file,
        '-vn', '-ab', '128k', '-ar', '44100', '-f', 'mp3', mp3_filename
    ])

    os.remove(downloaded_file)
    return mp3_filename


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("Downloading and converting, please wait...")

    try:
        filename = "audio_" + update.message.from_user.username
        mp3_file = await download_and_convert(url, filename)

        with open(mp3_file, 'rb') as audio:
            await update.message.reply_audio(audio)

        os.remove(mp3_file)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}. Make sure the link is valid.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot started...")
    app.run_polling()
