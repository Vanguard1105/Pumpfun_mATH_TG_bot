import requests
import json
import dotenv
import os
from solana.rpc.api import Client
from solders.pubkey import Pubkey


dotenv.load_dotenv()
BITQUERY_API_KEY=os.getenv("BITQUERY_API_KEY")

url = "https://streaming.bitquery.io/eap"

headers = {
   'Content-Type': 'application/json',
  #  'Authorization': f'Bearer ory_at_1flc7zw7xLWtSmSGuQ0-1jab0B8QFlTUOIMWR4yX25k.O57mDx0FIM-4cVSn6XVLcScYYjiDvtKejmT1drReZog',

   'X-API-KEY': BITQUERY_API_KEY,
}

def get_token_total_supply(token):
    # Connect to Solana's mainnet
    client = Client("https://api.mainnet-beta.solana.com")

    # Convert mint address string to Pubkey
    mint_pubkey = Pubkey.from_string(token)

    # Fetch token supply information
    response = client.get_token_supply(mint_pubkey)
    print(f"get_supply response: {response}")
    # Accessing the amount directly from the response object
    if response.value:
        amount = response.value.amount  # Accessing the amount attribute directly
        return float(amount)
    else:
        print("Failed to retrieve total supply. Please check the mint address.")
        return 0
    
def get_price(token):
  payload = json.dumps({
    "query": f"""
        {{
          Solana {{
            DEXTrades(
              where: {{Trade: {{Buy: {{Currency: {{MintAddress: {{is: "{token}"}}}}}}}}, Transaction: {{Result:{{Success: true}}}}}}
              limit: {{count: 1}}
              orderBy: {{descending: Block_Time}}
            ) {{
              Trade {{
                Buy {{
                  PriceInUSD
                }}
              }}
            }}
          }}
        }}
      """,
    "variables": "{}"
    })
  response = requests.request("POST", url, headers=headers, data=payload)
  print(response)
  print(f"get price response: {response.json()}")

  data = response.json()
  if data['data']['Solana']['DEXTrades'] == []: return 0
  return float(data['data']['Solana']['DEXTrades'][0]['Trade']['Buy']['PriceInUSD'])

def get_marketcap(token):
  price = get_price(token)
  if price < 0.00001: return price * 1000000000
  supply = get_token_total_supply(token)
  return price * supply / 1000000


