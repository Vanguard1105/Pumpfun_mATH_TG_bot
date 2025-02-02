import time
from pymongo import MongoClient
from get_mint_time_for_token import get_block_time
from get_traded_wallets_pumpfun_stage import get_traded_wallets_pumpfun_stage

# Connect to MongoDB
mongo_client = MongoClient("mongodb+srv://vanguard951105:F0Y7B0MtjvH1OFbL@cluster0.haemz.mongodb.net/")  
db = mongo_client["Pump"]  # Select the database named "Dexscreener"
all_wallets = db["All_traded_wallets_for_1m_tokens"]  # Select the collection named "wallet_data"
pump_wallets_collection = db['pumpfun_token-wallets']
all_wallets.delete_many({})
# Using a set to collect unique items
unique_items = set()

def save_all_wallets():
    wallets_traded_tokens = pump_wallets_collection.find().to_list()
    all_traded_wallets = []
    for obj in wallets_traded_tokens:
      for wallet in list(obj.values())[1]:
         if wallet != "" and wallet not in all_traded_wallets: all_traded_wallets.append(wallet)

    all_wallets.insert_one({'target_wallets': all_traded_wallets})
    print(f"Saved all traded wallets for all pumpfun tokens with 1m marketcap!")
