import requests
import dotenv
import os

dotenv.load_dotenv()
BITQUERY_API_KEY=os.getenv("BITQUERY_API_KEY")

def get_launch_time(token):
  BitQuery_url = "https://graphql.bitquery.io"
  headers = {
    # 'Authorization': f'Bearer ory_at_1flc7zw7xLWtSmSGuQ0-1jab0B8QFlTUOIMWR4yX25k.O57mDx0FIM-4cVSn6XVLcScYYjiDvtKejmT1drReZog',

    "X-API-KEY": BITQUERY_API_KEY
    }  # Set headers with Bitquery API key
  BITQUERY_query = """
    query MyQuery($token: String) {
      solana {
        transfers(
          currency: {is: $token}
          options: {limit: 1, asc: "block.timestamp.iso8601"}
          receiverAddress: {is: "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg"}
        ) {
          block {
            timestamp {
              iso8601
            }
          }
        }
      }
    }
    """
  variables = {"token": token}  # Prepare variables for GraphQL query with current pair address
  data = requests.post(BitQuery_url, json={"query": BITQUERY_query, "variables": variables}, headers=headers)
  print(f"get launch time response: {data.json()}")
  if data.status_code != 200: return "2020-01-01T00:00:00Z"
  data_json = data.json()
  print(data_json)
  if data_json['data']['solana']['transfers'] == []: return "2020-01-01T00:00:00Z"
  return data_json['data']['solana']['transfers'][0]['block']['timestamp']['iso8601']