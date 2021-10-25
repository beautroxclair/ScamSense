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

testWalletList = ["0x6306400da2b38c44d5dbe37097fba0d08ab6527c","0x1fc74c93d12d1ea9034dd87d601cf4d9f19202b8","0x55c6ecfdd1f8043537583a0f90ae40e1919aa966","0xda46f6ee5fca6c68f7d3be0e1758d9076e65c269","0x55dc4e8ed98ced86ec7d0ce6aae249af7a92f6be","0xc1713bbb86913e702dcd3fca2e0384be9e5c8aeb","0x27dce442debba17e71559378c9ad0ab7033af8c8","0x8e37b8970280d7d886d12a74e356fd559679fa61","0xa659cfb316e9f5d7210e0f331dcff02c3939713a","0x9301212e2d3a8122c66b4ed72e8a446e864aee82","0x022d130e57bb62d66cc404425cb4ce429b7cd952","0xe3cd7fcd06b4f3c61e93c9cdda791c263e16bffb","0x87cf7d52d5e16f936ce69b880bcec9860e7a9a4c","0xce1dfbf188adb8ead921e4e1e6553bd1ae7c19a6","0xef7c55bfb3ec25195bea3ffa944537b28815fa1c"]


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

	# Make First Call
	result = run_query(transferQuery, transferQueryParams)
	

	# Create CSVs with Headers
	with open("address.csv", "w") as addressCSV:
		writer = csv.writer(addressCSV)
		writer.writerow(['Public Key', 'Type', 'Kind'])

	with open("sends.csv", "w") as sendsCSV:
		writer = csv.writer(sendsCSV)
		writer.writerow(["Start_ID", "END_ID", "Type", "Amount", "Block", "Time", "hash"])


	walletsWithToken = set()
	smartContractSet = set()
	DEXset = set()
	Tokenset = set()
	iterations = 0

	# Iterate through all transactions in batches of "chunk"
	while True:

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
				# Needs Debugging - Not Getting all Transfers and I suspect the problem lies here

				if item["block"]["timestamp"]["iso8601"] > lastDate:
					lastDate = item["block"]["timestamp"]["iso8601"]

		newDateParam = {
			"network": "bsc",
			"token": token,
			"limit": chunk,
			"after": lastDate
		}

		result = run_query(transferQuery, newDateParam)
		

		iterations+=1
		print(iterations)
		print('--------------------')
		print(len(list(walletsWithToken)))
		print(len(list(DEXset)))
		print(len(list(smartContractSet)))
		print(len(list(Tokenset)))
		print('--------------------')
		print(len(result["data"]["ethereum"]["transfers"]))
		print('--------------------')
		

		if len(result["data"]["ethereum"]["transfers"]) != chunk or iterations > 7:

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

			break

	# Write Unique Addresses to CSV from sets
	with open("address.csv", "a") as addressCSV:
			writer = csv.writer(addressCSV)
			for item in list(walletsWithToken):
				writer.writerow([item,"Wallet","Personal"])
			for item in list(DEXset):
				writer.writerow([item,"Smart Contract","DEX"])
			for item in list(Tokenset):
				writer.writerow([item,"Smart Contract","Token"])
			for item in list(smartContractSet):
				writer.writerow([item,"Smart Contract","Generic"])





			


"""
----------------------------------------------------------------------
Get All Tokens
----------------------------------------------------------------------
"""
def get_all_tokens(walletList):

	tokenHoldingQuery = """
	query($tokenList: [String!])
	{
	  ethereum(network: bsc) {
	    address(
	      address: {in:$tokenList}
	    ) {
	      address
	      balances {
	        value
	        currency {
	          address
	          symbol
	        }
	      }
	    }
	  }
	}
	"""

	tokenQueryParams = {
		"tokenList": walletList
	}

	tokenResult = run_query(tokenHoldingQuery, tokenQueryParams)

	return tokenResult


	# with open("tokens.csv", "w") as tokensCSV:
	# 	writer = csv.writer(tokensCSV)
	# 	writer.writerow(["Token_ID", "Type", "Symbol"])

	# with open("owned.csv", "w") as ownedCSV:
	# 	writer = csv.writer(ownedCSV)
	# 	writer.writerow(["START_ID", "END_ID", "TYPE", "Amount"])



"""
----------------------------------------------------------------------
Query Execution 
----------------------------------------------------------------------
"""

# get_all_transfers(tokenAddress_MOONRISE,10000)
tokenQueryResult = get_all_tokens(testWalletList)
prettyResult = json.dumps(tokenQueryResult, indent = 2, sort_keys= True) # Print for Testing
print(prettyResult)
# result = run_query(tokenTransferQuery)  # Execute the query

# prettyResult = json.dumps(result, indent = 2, sort_keys= True) # Print for Testing
# print(prettyResult)

# export_to_csv(result) # Send to CSV Converter




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