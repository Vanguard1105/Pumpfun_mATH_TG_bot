import time
from pymongo import MongoClient
from get_mint_time_for_token import get_block_time
from get_traded_wallets_pumpfun_stage import get_traded_wallets_pumpfun_stage
from telegram_alert_all_pumpfun_tokens_with_1m import send_message_to_telegram
from datetime import datetime, timezone, timedelta
# Connect to MongoDB
mongo_client = MongoClient("mongodb+srv://vanguard951105:F0Y7B0MtjvH1OFbL@cluster0.haemz.mongodb.net/")  
db = mongo_client["Pump"]  # Select the database named "Dexscreener"
token_collection = db["pumpfun_tokens_with_over_mc_1m"]  # Select the collection named "wallet_data"
pump_wallets_collection = db['pumpfun_token-wallets']

def save_traded_wallets():
    pumpfun_tokens = token_collection.find().to_list()
    pump_wallets = pump_wallets_collection.find().to_list()
    for token in pumpfun_tokens:
        address = token["address"]
        traded_wallets = ["wallets"]
        for init in pump_wallets:
            if address in init:
                traded_wallets = ["already saved!"]
        if traded_wallets !=["wallets"]: 
            continue

        block_time = get_block_time(address)
        time.sleep(3)
        if block_time == "2023-06-17T01:39:22Z": traded_wallets = [""]
        else : 
          traded_wallets = get_traded_wallets_pumpfun_stage(address, block_time)
          time.sleep(3)
        # utc_now = datetime.now(timezone.utc) - timedelta(days=1) - timedelta(hours=6)
        # if block_time > utc_now: 
        #     message = f"""💞A new pump.fun token that was launched within 24 hours and already has a market cap of 1 million.💞\n"""
        #     message += f"💖 Symbol: <b>{token['symbol']}</b>     💰 MarketCap: <b>${token['marketcap']}</b>\n📍 <b>Address: <code>{token['address']}</code></b>\n\n"
        #     send_message_to_telegram(message)
        new_token = {
            "block_time": block_time,
            address: traded_wallets
        }
        pump_wallets_collection.insert_one(new_token)

    print(f"Saved all traded wallets in pumpfun stage for all tracked pumpfun token!")
