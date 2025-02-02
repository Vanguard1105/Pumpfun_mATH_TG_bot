import requests
import dotenv
import os

dotenv.load_dotenv()
BITQUERY_API_KEY=os.getenv("BITQUERY_API_KEY")

def get_traded_wallets_pumpfun_stage(token, time):
  BitQuery_url = "https://graphql.bitquery.io"
  headers = {
    # 'Authorization': f'Bearer ory_at_1flc7zw7xLWtSmSGuQ0-1jab0B8QFlTUOIMWR4yX25k.O57mDx0FIM-4cVSn6XVLcScYYjiDvtKejmT1drReZog',

    "X-API-KEY": BITQUERY_API_KEY
    } 
  BITQUERY_query = """
    query MyQuery ($token: String!, $time: ISO8601DateTime!){
      solana {
        transfers(
          currency: {is: $token}
          options: {asc: "block.timestamp.iso8601"}
          success: {is: true}
          time: {before: $time}
          ) {
          receiver {
            address
          }
          block {
            timestamp {
              iso8601
            }
          }
        }
      }
    }
    """
  variables = {"token": token, "time": time}  # Prepare variables for GraphQL query with current pair address
  data = requests.post(BitQuery_url, json={"query": BITQUERY_query, "variables": variables}, headers=headers) 
  print(f"get traded wallets response: {data}")

  if data.status_code != 200: return []
  data_json = data.json()
  result = []
  wallets = data_json['data']['solana']['transfers']
  for wallet in wallets:
    if wallet['receiver']['address'] not in result:
      result.append(wallet['receiver']['address'])

  return result
