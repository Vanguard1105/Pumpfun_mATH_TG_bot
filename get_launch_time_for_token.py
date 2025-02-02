import requests
import dotenv
import os

dotenv.load_dotenv()
BITQUERY_API_KEY=os.getenv("BITQUERY_API_KEY")

def get_launch_time(token):
  BitQuery_url = "https://graphql.bitquery.io"
  headers = {"X-API-KEY": BITQUERY_API_KEY}  # Set headers with Bitquery API key
  BITQUERY_query = """
    query MyQuery($token: String) {
      solana {
        transfers(
          currency: {is: $token}
          options: {limit: 1, asc: "block.timestamp.time"}
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
  print(f"get launch time response: {data}")

  data_json = data.json()
  if data_json['data']['solana']['transfers'] == None: return "2020-01-01T00:00:00Z"
  return data_json['data']['solana']['transfers'][0]['block']['timestamp']['iso8601']
