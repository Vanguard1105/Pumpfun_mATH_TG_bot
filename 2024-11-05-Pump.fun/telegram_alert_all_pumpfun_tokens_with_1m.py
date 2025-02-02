import requests
from pymongo import MongoClient
from datetime import datetime
import time
import random


# Connect to MongoDB
mongo_client = MongoClient("mongodb+srv://vanguard951105:F0Y7B0MtjvH1OFbL@cluster0.haemz.mongodb.net/")  
db = mongo_client["Pump"]  # Select the database named "Dexscreener"
token_collection = db["result_data"]  # Select the collection named "wallet_data"
result_data = token_collection.find().sort("marketcap", -1).to_list()

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
  print(response)
  time.sleep(random.uniform(3, 4))
def alert_tokens():
  today = datetime.now().strftime("%B %d, %Y")
  message = f"""<b>💞 Pump fun Token Update!     📅 {today} 💞
The following tokens launched within 24 hours have already 
surpassed 1 million in market cap:💰📈
🔍 Total Tokens: {len(result_data)}</b>\n"""
  send_message_to_telegram(message)
  index_token = 1
  for token in result_data:
    date_obj = datetime.fromisoformat(str(token['mint_time']))
    formatted_marketcap = "{:,.2f}".format(token['marketcap'])
    formatted_date = date_obj.strftime("%A, %B %d, %Y at %I:%M %p")
    formatted_index_token = f"{index_token:02}"
    message = f"""
    📈 Rank: <b>{formatted_index_token}</b>\n💖 Mint Date: <b>{formatted_date}</b>
💰 MarketCap: <b>${formatted_marketcap}</b>
📍 Address: <code>{token['token']}</code>\n
🚀 The following wallets have actively traded this token during the
    exhilarating Pump Fun Stage! 💰✨
🔍 Total wallets: {len(token['traded_wallets'])}"""
    index_token += 1
    send_message_to_telegram(message)
    wallet_index = 1
    message = ""
    for wallet in token['traded_wallets']:
      formatted_index_wallet = f"{wallet_index:03}"
      message += f"<b>{formatted_index_wallet}: </b> <code>{wallet}</code>\n"
      if wallet_index % 50 == 0: 
        send_message_to_telegram(message)
        message = ""
      wallet_index += 1
    if wallet_index % 50 != 1: send_message_to_telegram(message)
alert_tokens()