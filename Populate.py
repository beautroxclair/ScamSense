	 import requests
import json
import csv
import math


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
- 502 Error - Ran out of Memory
- 504 Error - Timeout
-- Functionality to switch between API Keys if request limit has been reached


----------------------------------------------------------------------
"""
##API KEY - BQY9Rwp5LBgFHnp440ilWi0xk7tUxIZQ

def run_query(query, variables = {}):  # A simple function to use requests.post to make the API call.
    headers = {'X-API-KEY': 'YOUR_API_KEY'}
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
	lastDate = result["data"]["ethereum"]["transfers"][0]["block"]["timestamp"]["iso8601"]

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

		if result["data"]["ethereum"]["transfers"][0]["block"]["timestamp"]["iso8601"] is None:
			print(result)
			pass
		else:
			lastDate = result["data"]["ethereum"]["transfers"][0]["block"]["timestamp"]["iso8601"]


			# Write Sends and Extract Addresses
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

				print("---------------")
				print("Query {}: {}".format(iterations+1,lastDate))
				iterations+=1


		newDateParam = {
			"network": "bsc",
			"token": token,
			"limit": chunk,
			"after": lastDate
		}

		try:
			result = run_query(transferQuery, newDateParam)
			if result["data"]["ethereum"]["transfers"][0]["block"]["timestamp"]["iso8601"] is None:
				print(result)
				pass
			else:
		
				if len(result["data"]["ethereum"]["transfers"]) != chunk or iterations >= 200:

					print("---------------")
					print("Query {}: {}".format(iterations+1,lastDate))

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


					print("---------------")
					print("---------------")
					break

		except:
			pass

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

	return list(walletsWithToken)




			


"""
----------------------------------------------------------------------
Get All Tokens
----------------------------------------------------------------------
"""
def get_all_tokens(walletList):

	# Initialize the CSVs
	with open("tokens.csv", "w") as tokensCSV:
		writer = csv.writer(tokensCSV)
		writer.writerow(["Token_ID", "Type", "Symbol"])

	with open("owned.csv", "w") as ownedCSV:
		writer = csv.writer(ownedCSV)
		writer.writerow(["START_ID", "END_ID", "TYPE", "Amount"])

	tokens = []
	trigger = False


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


	# Execute Query in chunks of 250
	for i in range(math.ceil(len(walletList)/250)):
		
		tokenQueryParams = None

		if i*250+250 > len(walletList):
			tokenQueryParams = {
				"tokenList": walletList[i*250:]
			}
		else:
			tokenQueryParams = {
				"tokenList": walletList[i*250:i*250+250]
			}
		print("---------------")
		print("Query {} of {}".format(i+1,math.ceil(len(walletList)/250)))
		try:
			tokenResult = run_query(tokenHoldingQuery, tokenQueryParams)
			tokens = write_token_chunk(tokenResult,tokens)
		except:
			print("Query {} of {} failed".format(i+1,math.ceil(len(walletList)/250)))
			try:
				print("Query {} of {} retry".format(i+1,math.ceil(len(walletList)/250)))
				tokenResult = run_query(tokenHoldingQuery, tokenQueryParams)
				tokens = write_token_chunk(tokenResult,tokens)
			except:
				print("Query {} of {} failed again".format(i+1,math.ceil(len(walletList)/250)))
				if trigger == False:
					with open("errors.csv","w") as errorsCSV:
						errorWriter = csv.writer(errorsCSV)
						for j in walletList[i*250:i*250+250]:
							errorWriter.writerow([j])
				else:
					with open("errors.csv","a") as errorsCSV:
						errorWriter = csv.writer(errorsCSV)
						for j in walletList[i*250:i*250+250]:
							errorWriter.writerow([j])
				trigger = True
				pass
			pass

	with open("tokens.csv", "a") as tokensCSV:
		writer = csv.writer(tokensCSV)
		for item in tokens:
			writer.writerow([item["address"],"TOKEN",item["symbol"]])
	print("---------------")
	print("---------------")

def write_token_chunk(chunk,tokenList):
	with open("owned.csv","a") as ownedCSV:
		writer = csv.writer(ownedCSV)
		for item in chunk["data"]["ethereum"]["address"]:
			for obj in item["balances"]:

				if obj["value"] > 0:
					writer.writerow([item["address"],obj["currency"]["address"],"OWNS",obj["value"]])
				else:
					writer.writerow([item["address"],obj["currency"]["address"],"OWNED",obj["value"]])

				tokenList.append({"address":obj["currency"]["address"],"symbol":obj["currency"]["symbol"]})


				# prettyObj = json.dumps(obj, indent = 2, sort_keys= True) # Print for Testing
				# print(prettyObj)

	tokenList = list({v['address']:v for v in tokenList}.values())

	return tokenList


# Test

# tokenResult = run_query(tokenHoldingQuery, tokenQueryParams)
# return tokenResult


	


"""
----------------------------------------------------------------------
Query Execution 
----------------------------------------------------------------------
"""

walletList = get_all_transfers(tokenAddress_SAFEMOON,10000)
get_all_tokens(walletList)



# prettyResult = json.dumps(allTokens, indent = 2, sort_keys= True) # Print for Testing
# with open("tokens.json", "w") as outfile:
#     outfile.write(prettyResult)



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


LOAD CSV WITH HEADERS FROM "file:///address.csv" AS row
MERGE (a:Address {public_key: row["Public Key"],type:row["Type"],kind:[row["Kind"]]})

LOAD CSV WITH HEADERS FROM "file:///tokensTransformed.csv" AS row
CREATE (t:Token {token_id: row["Token_ID"],type:row["Type"],symbol:[row["Symbol"]]})

LOAD CSV WITH HEADERS FROM "file:///sends.csv" AS row
MATCH (a:Address {public_key: row["Start_ID"]})
MATCH (b:Address {public_key: row["END_ID"]})
CREATE (a)-[:SEND {amount:row["Amount"], block:row["Block"], time:row["Time"], hash:row["hash"]}]->(b)

----------------------------------------------------------------------
"""


"""
----------------------------------------------------------------------
Queries to be implemented
----------------------------------------------------------------------


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

Parallelization:
https://medium.com/swlh/parallel-asynchronous-api-call-in-python-f6aa663206c6

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