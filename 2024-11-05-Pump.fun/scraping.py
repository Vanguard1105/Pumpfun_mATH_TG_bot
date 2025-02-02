import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
import re
from pymongo import MongoClient

mongo_client = MongoClient("mongodb+srv://vanguard951105:F0Y7B0MtjvH1OFbL@cluster0.haemz.mongodb.net/")  
db = mongo_client["Pump"]  # Select the database named "Dexscreener"
token_collection = db["pump-radyum"]  # Select the collection named "pump-radyum"
# Load environment variables from .env file
load_dotenv()

const1 = os.getenv('API_ID')
const2 = os.getenv('API_HASH')

source_channel = 'trackerchannelsdiscussion'  
client = TelegramClient('bot', const1, const2)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    message_text = event.message
    match = re.search(r'([A-Za-z0-9]{44})', message_text.message)
    if match:
        print(match.group(0))  # This will print the matched code
        token_collection.insert_one({"token": match.group(0)})

print("Bot is now running...")
with client:
    client.run_until_disconnected()