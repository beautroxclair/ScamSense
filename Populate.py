import requests
import json
import csv


tokenAddress = "0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3"

"""
----------------------------------------------------------------------

Simple Query Post Function with API Key Included
To Add:
- better error handling for status code responses
-- Functionality to switch between API Keys if request limit has been reached

----------------------------------------------------------------------
"""


def run_query(query):  # A simple function to use requests.post to make the API call.
    headers = {'X-API-KEY': 'BQYq2Lq2oo8E55XwYQkCwb8zfA3kb4QT'}
    request = requests.post('https://graphql.bitquery.io/',
                            json={'query': query}, headers=headers)
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

			writer1.writerow([':ID', ':LABEL'])
			writer2.writerow([':START_ID', ':END_ID', ":TYPE", "amount:float", "block", "time", "hash"])

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
      options: {limit: 20, asc: "block.height"}
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



"""
----------------------------------------------------------------------
Query Execution 
----------------------------------------------------------------------
"""

result = run_query(tokenTransferQuery)  # Execute the query
export_to_csv(result)




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

LOAD CSV WITH HEADERS FROM "file///transfers.csv" AS row
MATCH (s:Sender {wallet_id: row[":START_ID"]})
MATCH (r:Receiver {wallet_id: row[":END_ID"]})
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

Neo4j and Machine Learning:
https://neo4j.com/blog/liberating-knowledge-machine-learning-techniques-neo4j/

Great Video on Neo4j Imports:
https://www.youtube.com/watch?v=oXziS-PPIUA
https://github.com/johnymontana/neo4j-datasets/tree/master/yelp/src

GraphQL Query Structure IDE:
https://graphql.bitquery.io/ide



"""