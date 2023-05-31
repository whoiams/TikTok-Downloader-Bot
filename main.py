import os
from telegram.ext import Updater, CommandHandler
import requests

# Define your Telegram bot token
TOKEN = '6162835664:AAF82yhi5W7jJe8VJxeLTk10xKGCLWBn6Fk'

# Define the command handler for the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the TikTok downloader bot!")

# Define the command handler for the /download command
def download(update, context):
    # Check if a URL is provided as an argument
    if len(context.args) > 0:
        url = context.args[0]
        
        # Send a message indicating the download has started
        context.bot.send_message(chat_id=update.effective_chat.id, text="Downloading TikTok video...")
        
        # Download the TikTok video using requests library
        response = requests.get(url, stream=True)
        
        # Get the filename from the URL
        filename = os.path.basename(url)
        
        # Save the video to a file
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        
        # Send the downloaded video file
        context.bot.send_video(chat_id=update.effective_chat.id, video=open(filename, 'rb'))
        
        # Remove the downloaded video file
        os.remove(filename)
        
    else:
        # Send an error message if no URL is provided
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a TikTok video URL.")

# Create an instance of the Updater class and pass it the Telegram bot token
updater = Updater(token=TOKEN, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the command handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("download", download))

# Start the bot
updater.start_polling()
