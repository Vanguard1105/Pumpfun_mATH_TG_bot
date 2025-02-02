from get_mint_time_for_token import get_mint_time
from get_marketcap_for_token import get_marketcap
from get_launch_time_for_token import get_launch_time
from get_traded_wallets_pumpfun_stage import get_traded_wallets_pumpfun_stage
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient

mongo_client = MongoClient("mongodb+srv://vanguard951105:F0Y7B0MtjvH1OFbL@cluster0.haemz.mongodb.net/")  
db = mongo_client["Pump"]  # Select the database named "Dexscreener"
token_collection = db["pump-radyum"]  # Select the collection named "wallet_data"
result_data = db["result_data"]
# result_data.delete_many({})

possible_tokens = token_collection.find().to_list()

def save_target_tokens():
  index_t = 1
  for token in possible_tokens:
    print(f"token-->: {index_t}")
    index_t += 1
    

    marketcap = get_marketcap(token['token'])
    print(marketcap)
    if marketcap < 1000000: 
      token_collection.delete_many({"token": token['token']})
      continue

    response_time = get_mint_time(token['token'])
    mint_time = datetime.fromisoformat(response_time.replace("Z", "+00:00"))
    current_time = datetime.now(timezone.utc) + timedelta(hours=6)
    time_difference = current_time - mint_time
    if time_difference.days: 
      token_collection.delete_many({"token": token['token']})
      continue
    print(token['token'])
    launch_time = get_launch_time(token['token'])

    if launch_time == "2020-01-01T00:00:00Z": 
      token_collection.delete_many({"token": token['token']})
      continue
    traded_wallets = get_traded_wallets_pumpfun_stage(token['token'], launch_time)

    result_data.insert_one({
      "token": token['token'],
      "mint_time": mint_time,
      "marketcap": marketcap,
      "traded_wallets": traded_wallets
      })
    
    print(token['token'], mint_time, time_difference.days, marketcap, len(traded_wallets))
    print("\n")
    # if time_difference.days==0 and time_difference.seconds < 10000: continue
    token_collection.delete_many({"token": token['token']})

save_target_tokens()