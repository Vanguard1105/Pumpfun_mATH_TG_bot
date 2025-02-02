import requests
from pymongo import MongoClient
from datetime import datetime
import time
today = datetime.now().strftime("%B %d, %Y")

# Connect to MongoDB
mongo_client = MongoClient("mongodb+srv://vanguard951105:F0Y7B0MtjvH1OFbL@cluster0.haemz.mongodb.net/")  
db = mongo_client["Pump"]  # Select the database named "Dexscreener"
token_collection = db["pumpfun_tokens_with_over_mc_1m"]  # Select the collection named "wallet_data"
wallets_traded_tokens = token_collection.find().sort("marketcap", -1).to_list()

def send_message_to_telegram(message):
  bot_token = '7762867827:AAG9PEh9DFabFxE_KD6COWQeBVr5wq2oKeU' # Telegram bot(Bitcoin Lottery) token (replace with your own)
  chat_id = "@pumpfun_alert_ch"
  url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

  # Parameters for the request
  params = {
      'chat_id': chat_id,
      'text': message,
      'parse_mode': 'HTML',
      'disable_web_page_preview': True  # Disable link previews
  }
  response = requests.get(url, params=params)

def alert_tokens(tokens):
  message = f"""<b>💞 Pump fun Token Update!     📅 {today} 💞
The following Pump fun tokens have achieved a market cap of $1 million
or more!💰📈
🔍 Total Tokens: {len(tokens)}</b>\n"""
  send_message_to_telegram(message)
  index = 0
  message = f"""<b>🏆 Here is the token information from {index + 1} ~ {20}th place in the ranking.</b>\n\n"""
  for token in tokens:
    if index and index % 20 == 0:
      send_message_to_telegram(message)
      if index + 20 > len(tokens): to = len(tokens)
      else: to = index + 20
      message = f"""<b>🏆 Here is the token information from {index + 1} ~ {to}th place in the ranking.</b>\n\n"""
    index += 1
    message += f"📈 Rank: <b>{index}</b>\n💖 Symbol: <b>{token['symbol']}</b>     💰 MarketCap: <b>${token['marketcap']}</b>\n📍 <b>Address: <code>{token['address']}</code></b>\n\n"
  if index % 20 != 1:
    send_message_to_telegram(message)