import requests
import json
tokenAddress = "0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3"

# given the above token address GET list of wallets and GET list of transactions


def run_query(query):  # A simple function to use requests.post to make the API call.
    headers = {'X-API-KEY': 'BQYq2Lq2oo8E55XwYQkCwb8zfA3kb4QT'}
    request = requests.post('https://graphql.bitquery.io/',
                            json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.      {}'.format(request.status_code,
                        query))


# The GraphQL query

query = """
{
  ethereum(network: bsc) {
    transfers(
      currency: {is: "0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3"}
      options: {limit: 100000, asc: "block.height"}
    ) 
    {
      amount
      receiver {
        address
      }
      sender {
        address
      }
      block {
        timestamp {
          time
        }
        height
      }
      transaction {
        hash
      }
    }
  }
}
"""
result = run_query(query)  # Execute the query
prettyResult = json.dumps(result, indent = 4, sort_keys= True)

with open("transfers.json", "w") as outfile:
    outfile.write(prettyResult)


# Token Transfers
# {
#   ethereum(network: bsc) {
#     transfers(
#       currency: {is: "0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3"}
#       options: {limit: 10}
#     ) {
#       amount
#       receiver {
#         address
#       }
#       sender {
#         address
#       }
#       block {
#         timestamp {
#           time
#         }
#         height
#       }
#       transaction {
#         hash
#       }
#       count
#     }
#   }
# }

#  DEX Trades
# {
# 	ethereum(network: bsc){
# 		dexTrades(options: {limit: 100, desc: "block.height"}, exchangeName: {in:["Pancake","Pancake v2"]},
# 		baseCurrency: {is: "0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3"})
# 		{
# 			transaction {
# 				hash
# 			}
# 			smartContract{
# 				address{
# 					address
# 				}
# 				contractType
# 				currency{
# 					name
# 				}
# 			}
# 			tradeIndex
# 			date {
# 				date
# 			}
# 			block {
# 				height
# 			}
# 			buyAmount
# 			buyAmountInUsd: buyAmount(in: USD)
# 			buyCurrency {
# 				symbol
# 				address
# 			}
# 			sellAmount
# 			sellAmountInUsd: sellAmount(in: USD)
# 			sellCurrency {
# 				symbol
# 				address
# 			}
# 			sellAmountInUsd: sellAmount(in: USD)
# 			tradeAmount(in: USD)
# 			transaction{
# 				gasValue
# 				gasPrice
# 				gas
# 			}
# 		}
# 	}
# }

#Pool Info
# smartContractAddress:
# {is:"0x1b96b92314c44b159149f7e0303511fb2fc4774f"},
# date: {since:"2020-12-12", till: "2020-12-12"}
# ){
# count
# tradeAmount(in:USD)
# }}
# }

# Pool Info Date wise
# {
# ethereum (network: bsc){
# dexTrades(options: {desc: "date.date"},
# smartContractAddress:
# {is:"0x1b96b92314c44b159149f7e0303511fb2fc4774f"}
# ){
# count
# tradeAmount(in:USD)
# date{
# date(format: "%y-%m-%d")
# }}
# }}

# All Trades of a pool
# {
# ethereum(network: bsc){
# dexTrades(options: {limit: 1, desc: "block.height"},
# exchangeName: {in:["Pancake","Pancake v2"]},
# smartContractAddress: {is: "0x1b96b92314c44b159149f7e0303511fb2fc4774f"}){
# transaction {
# hash
# }
# smartContract{
# address{
# address
# }
# contractType
# currency{
# name
# }}
# tradeIndex
# date {
# date
# }
# block {
# height
# }
# buyAmount
# buyAmountInUsd: buyAmount(in: USD)
# buyCurrency {
# symbol
# address
# }
# sellAmount
# sellAmountInUsd: sellAmount(in: USD)
# sellCurrency {
# symbol
# address
# }
# sellAmountInUsd: sellAmount(in: USD)
# tradeAmount(in: USD)
# transaction{
# gasValue
# gasPrice
# gas
# }}
# }}



