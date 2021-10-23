import requests
import json
import csv


tokenAddress_SAFEMOON= "0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3" #9.29mil transfers
tokenAddress_SAFEMOONCASH = "0xf017e2773e4ee0590c81d79ccbcf1b2de1d22877" # 891k transfers
tokenAddress_SLIME = "0x4fcfa6cc8914ab455b5b33df916d90bfe70b6ab1" # 863k Transfers
tokenAddress_FOX = "0xfad8e46123d7b4e77496491769c167ff894d2acb" #435k Transfers
tokenAddress_WOOF = "0x9e26c50b8a3b7652c3fd2b378252a8647a0c9268" #440k Transfers "Shibance token"
tokenAddress_POOCOIN = "0xb27adaffb9fea1801459a1a81b17218288c097cc" #433k Transfers
tokenAddress_PORNROCKET = "0xcf9f991b14620f5ad144eec11f9bc7bf08987622" #419k Transfers
tokenAddress_CROW = "0xcc2e12a9b5b75360c6fbf23b584c275d52cddb0e" # 405k Transfers
tokenAddress_DaddyDoge = "0x7cce94c0b2c8ae7661f02544e62178377fe8cf92" #227k Transfers
tokenAddress_SAFETESLA = "0xa1efce38cb265af369e891bc3026d0285545d4e5" #219k Transfers
tokenAddress_SOUPS = "0x69f27e70e820197a6e495219d9ac34c8c6da7eee" #218k transfers
tokenAddress_PASTA = "0xab9d0fae6eb062f2698c2d429a1be9185a5d4f6e" #212k transfers
tokenAddress_PirateCoin = "0x041640ea980e3fe61e9c4ca26d9007bc70094c15" # 211k transfers
tokenAddress_WEAPON = "0x3664d30a612824617e3cf6935d6c762c8b476eda" #178k Transfers
tokenAddress_MOONRISE = "0x7ee7f14427cc41d6db17829eb57dc74a26796b9d" #187k Transfers


"""
----------------------------------------------------------------------

Simple Query Post Function with API Key Included
To Add:
- better error handling for status code responses
-- Functionality to switch between API Keys if request limit has been reached

----------------------------------------------------------------------
"""


def run_query(query, variables = {}):  # A simple function to use requests.post to make the API call.
    headers = {'X-API-KEY': 'BQYq2Lq2oo8E55XwYQkCwb8zfA3kb4QT'}
    request = requests.post('https://graphql.bitquery.io/',
                            json={'query': query, 'variables': variables}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.      {}'.format(request.status_code,
                        query))


"""
----------------------------------------------------------------------
JSON -> CSV Conversion Module
----------------------------------------------------------------------
"""


def export_to_csv(data):

	with open("wallets.csv", "w") as walletsCSV:
		with open("sends.csv", "w") as sendsCSV:
			writer1 = csv.writer(walletsCSV)
			writer2 = csv.writer(sendsCSV)

			writer1.writerow(['Public Key', 'Type', 'Tokens Held'])
			writer2.writerow([':START_ID', ':END_ID', ":TYPE"])

			for item in data["data"]["ethereum"]["transfers"]:

				amount = item["amount"]
				block = item["block"]["height"]
				timestamp = item["block"]["timestamp"]["time"]
				receiver = item["receiver"]["address"]
				sender = item["sender"]["address"]
				txHash = item["transaction"]["hash"]

				writer1.writerow([sender, "WALLET"])
				writer1.writerow([receiver, "WALLET"])

				writer2.writerow([sender, receiver, "SEND", amount, block, timestamp, txHash])
				


"""
----------------------------------------------------------------------
Get All Transfers
----------------------------------------------------------------------
"""
def get_all_transfers(token, chunk):

	#Define Query and Paramaters
	transferQuery = """
		query ($network: EthereumNetwork!, $token: String!, $limit: Int!, $after: ISO8601DateTime){
			ethereum(network: $network) {
				transfers(
					currency: {is:$token}
					options: {
						limit: $limit
				        asc: "date.date"
				        desc: "block.timestamp.iso8601"
					}
					date: {after: $after}	
				){
					amount
					receiver {
						address
						smartContract {
							contractType
						}
					}
					sender {
						address
						smartContract {
							contractType
						}
					}
					block {
						timestamp {
							iso8601
						}
						height
					}
					date {
						date
					}
					transaction {
						hash
					}
				}
			}
		}

	"""

	transferQueryParams = {
		"network": "bsc",
		"token": token,
		"limit": chunk,
		"after": None
	}

	# # Make First Call
	# result = run_query(transferQuery, transferQueryParams)

	# # Testing
	# prettyResult = json.dumps(result, indent = 4, sort_keys= True)

	# with open("transfers.json", "w") as outfile:
	#     outfile.write(prettyResult)

	
	#Write to CSV
	with open("transfers.json", "r") as file:

		# Create CSVs with Headers
		with open("address.csv", "w") as addressCSV:
			writer = csv.writer(addressCSV)
			writer.writerow(['Public Key', 'Type', 'Kind'])

		with open("sends.csv", "w") as sendsCSV:
			writer = csv.writer(sendsCSV)
			writer.writerow(["Start_ID", "END_ID", "Type", "Amount", "Block", "Time", "hash"])


		result= json.load(file)
		iterations = 0
		while(len(result["data"]["ethereum"]["transfers"]) == chunk and iterations < 1):

			walletsWithToken = set()
			smartContractSet = set()
			DEXset = set()
			Tokenset = set()

			lastDate = result["data"]["ethereum"]["transfers"][0]["block"]["timestamp"]["iso8601"]

			with open("sends.csv", "a") as sendsCSV:
				writer = csv.writer(sendsCSV)

				for item in result["data"]["ethereum"]["transfers"]:


					# Write to sends.csv

					writer.writerow([
						item["sender"]["address"],
						item["receiver"]["address"],
						"SEND",
						item["amount"],
						item["block"]["height"],
						item["block"]["timestamp"]["iso8601"],
						item["transaction"]["hash"]
					])


					# Separate Different Address Types into unique sets

					if item["receiver"]["smartContract"]["contractType"] is None:
						walletsWithToken.add(item["receiver"]["address"])
					elif item["receiver"]["smartContract"]["contractType"] == "DEX":
						DEXset.add(item["receiver"]["address"])
					elif item["receiver"]["smartContract"]["contractType"] == "Token":
						Tokenset.add(item["receiver"]["address"])
					else:
						smartContractSet.add(item["receiver"]["address"])

					if item["sender"]["smartContract"]["contractType"] is None:
						walletsWithToken.add(item["sender"]["address"])
					elif item["sender"]["smartContract"]["contractType"] == "DEX":
						DEXset.add(item["sender"]["address"])
					elif item["sender"]["smartContract"]["contractType"] == "Token":
						Tokenset.add(item["sender"]["address"])
					else:
						smartContractSet.add(item["sender"]["address"])

					# Perform Date Check

					if item["block"]["timestamp"]["iso8601"] > lastDate:
						lastDate = item["block"]["timestamp"]["iso8601"]


			print(len(list(walletsWithToken)))
			print(len(list(DEXset)))
			print(len(list(smartContractSet)))
			print(len(list(Tokenset)))

			iterations+=1


"""
----------------------------------------------------------------------
Get All Tokens
----------------------------------------------------------------------
"""
def get_all_tokens(walletList):

	with open("tokens.csv", "w") as tokensCSV:
		writer = csv.writer(tokensCSV)
		writer.writerow(["Token_ID", "Type", "Symbol"])

	with open("has.csv", "w") as hasCSV:
		writer = csv.writer(hasCSV)
		writer.writerow(["START_ID", "END_ID", "TYPE", "Amount"])



"""
----------------------------------------------------------------------
Query Execution 
----------------------------------------------------------------------
"""

get_all_transfers(tokenAddress_SAFEMOON,2000)

# result = run_query(tokenTransferQuery)  # Execute the query

# prettyResult = json.dumps(result, indent = 2, sort_keys= True) # Print for Testing
# print(prettyResult)

# export_to_csv(result) # Send to CSV Converter







"""
----------------------------------------------------------------------
GraphQL Query Definitions
----------------------------------------------------------------------
"""


# Returns token transfers ascending by block with hard coded limit 
# Tested and working up to 100,000 results but more may be possible in single query

tokenTransferQuery = """
{
  ethereum(network: bsc) {
    transfers(
      currency: {is: "0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3"}
      options: {limit: 10, asc: "block.height"}
    ) 
    {
      amount
      receiver {
        address
        smartContract{
        	contractType
        }
      }
      sender {
        address
        smartContract{
        	contractType
        }
      }
      block {
        timestamp {
          iso8601
        }
        height
      }
    }
  }
}
"""

tokenHoldingQuery = """
($tokenList: [String!])
{
  ethereum(network: bsc) {
    address(
      address: {in:$tokenList}
    ) {
      address
      smartContract {
        contractType
      }
      balances {
        value
        currency {
          address
          symbol
          tokenType
        }
      }
    }
  }
}
"""


"""
----------------------------------------------------------------------
Upload Module
----------------------------------------------------------------------
"""

# TODO
#	Not sure if we need an inline upload, may accomplish this on the command line, but may be nice to code in here
#	If for no other reason then we don't have to deal with compatibility Issues
#	Will Certainly be necessary if we host the DB in the cloud

"""
----------------------------------------------------------------------
Naiive Load commands in Neo4j Desktop


LOAD CSV WITH HEADERS FROM "file:///wallets.csv" AS row
MERGE (w:Wallet {wallet_id: row[":ID"]})

LOAD CSV WITH HEADERS FROM "file:///sends.csv" AS row
MATCH (s:Wallet {wallet_id: row[":START_ID"]})
MATCH (r:Wallet {wallet_id: row[":END_ID"]})
CREATE (s)-[:SEND {amount:row["amount:float"], block:row.block, time:row.time, hash:row.hash}]->(r)

----------------------------------------------------------------------
"""


"""
----------------------------------------------------------------------
Queries to be implemented
----------------------------------------------------------------------


Token Transfers
{
  ethereum(network: bsc) {
    transfers(
      currency: {is: "0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3"}
      options: {limit: 10}
    ) {
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
      count
    }
  }
}

Token Amounts of Wallets
{
  ethereum(network: bsc) {
    address(
      address: {in: ["0xff3dd404afba451328de089424c74685bf0a43c9", "0xacf29a85e341c7fb05d2755e2f83c36afe5cfeeb", "0x8c128dba2cb66399341aa877315be1054be75da8"]}
    ) {
      address
      smartContract {
        contractType
      }
      balances {
        value
        currency {
          address
          symbol
          tokenType
        }
      }
    }
  }
}


Possibe Responses:(?)

{
  "ethereum": {
    "address": [
      {
        "address": "0xff3dd404afba451328de089424c74685bf0a43c9",
        "smartContract": {
          "contractType": "DEX"
        }
      },
      {
        "address": "0xacf29a85e341c7fb05d2755e2f83c36afe5cfeeb",
        "smartContract": null
      },
      {
        "address": "0x8c128dba2cb66399341aa877315be1054be75da8",
        "smartContract": {
          "contractType": "Generic"
        }
      }
    ]
  }
}



DEX Trades
{
	ethereum(network: bsc){
		dexTrades(options: {limit: 100, desc: "block.height"}, exchangeName: {in:["Pancake","Pancake v2"]},
		baseCurrency: {is: "0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3"})
		{
			transaction {
				hash
			}
			smartContract{
				address{
					address
				}
				contractType
				currency{
					name
				}
			}
			tradeIndex
			date {
				date
			}
			block {
				height
			}
			buyAmount
			buyAmountInUsd: buyAmount(in: USD)
			buyCurrency {
				symbol
				address
			}
			sellAmount
			sellAmountInUsd: sellAmount(in: USD)
			sellCurrency {
				symbol
				address
			}
			sellAmountInUsd: sellAmount(in: USD)
			tradeAmount(in: USD)
			transaction{
				gasValue
				gasPrice
				gas
			}
		}
	}
}

Pool Info
smartContractAddress:
{is:"0x1b96b92314c44b159149f7e0303511fb2fc4774f"},
date: {since:"2020-12-12", till: "2020-12-12"}
){
count
tradeAmount(in:USD)
}}
}

Pool Info Date wise
{
ethereum (network: bsc){
dexTrades(options: {desc: "date.date"},
smartContractAddress:
{is:"0x1b96b92314c44b159149f7e0303511fb2fc4774f"}
){
count
tradeAmount(in:USD)
date{
date(format: "%y-%m-%d")
}}
}}

All Trades of a pool
{
ethereum(network: bsc){
dexTrades(options: {limit: 1, desc: "block.height"},
exchangeName: {in:["Pancake","Pancake v2"]},
smartContractAddress: {is: "0x1b96b92314c44b159149f7e0303511fb2fc4774f"}){
transaction {
hash
}
smartContract{
address{
address
}
contractType
currency{
name
}}
tradeIndex
date {
date
}
block {
height
}
buyAmount
buyAmountInUsd: buyAmount(in: USD)
buyCurrency {
symbol
address
}
sellAmount
sellAmountInUsd: sellAmount(in: USD)
sellCurrency {
symbol
address
}
sellAmountInUsd: sellAmount(in: USD)
tradeAmount(in: USD)
transaction{
gasValue
gasPrice
gas
}}
}}

"""


"""
----------------------------------------------------------------------
Resources
----------------------------------------------------------------------

Cypher Query Documentation:
https://neo4j.com/developer/cypher/
https://neo4j.com/docs/cypher-manual/current/clauses/

Neo4j Importing From Dump
https://tbgraph.wordpress.com/2020/11/11/dump-and-load-a-database-in-neo4j-desktop/

Neo4j and Machine Learning:
https://neo4j.com/blog/liberating-knowledge-machine-learning-techniques-neo4j/

Great Video on Neo4j Imports:
https://www.youtube.com/watch?v=oXziS-PPIUA
https://github.com/johnymontana/neo4j-datasets/tree/master/yelp/src

GraphQL Query Structure IDE:
https://graphql.bitquery.io/ide





"""