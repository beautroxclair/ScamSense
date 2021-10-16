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
	ethereum(network: bsc){
		dexTrades(options: {limit: 5, desc: "block.height"},
		exchangeName: {in:["Pancake","Pancake v2"]}
		baseCurrency: {is: "0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3"}){
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
"""
result = run_query(query)  # Execute the query
prettyResult = json.dumps(result, indent = 2, sort_keys= True)
print(prettyResult)



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


#Neo4j activation Key
eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Ii4rQC4rIiwibWl4cGFuZWxJZCI6IjE3YzQzYmZiNzI5MTI2NC0wYTdiYTViOGU5OTNlZi0xYzNiNjY1MC0xM2M2ODAtMTdjNDNiZmI3MmExNjQ3IiwibWl4cGFuZWxQcm9qZWN0SWQiOiI0YmZiMjQxNGFiOTczYzc0MWI2ZjA2N2JmMDZkNTU3NSIsIm9yZyI6Ii4qIiwicHViIjoibmVvNGouY29tIiwicmVnIjoiICIsInN1YiI6Im5lbzRqLWRlc2t0b3AiLCJleHAiOjE2NjU1MzcwMDAsInZlciI6IioiLCJpc3MiOiJuZW80ai5jb20iLCJuYmYiOjE2MzQwMDEwMDAsImlhdCI6MTYzNDAwMTAwMCwianRpIjoiTnphbWpvZml5In0.MYU2lvpGk_qagAlpquDzPYmbfePAfXooAN8K8osptnI0xYu7fHFxkkrT-1gN9QjsnDBc45r6cfygtJGVufdpeAhA9EC7QcS8kOkpdOjQdcnE3U9Hk43Ctr6MRLM6uFPenPlyLdwiOyyynmu5uqTVFg_86_-KoFqw7WJ0Gk49fRFK7G4_NzS-CMw9EOSYMH0SElzK2nN1a4U31vhIBFAKhqvunwaFo1mlzyX1Q6c8-y8P-puR2HMdze3HhS3YsaxqWIs3jfDWESTOd8xukQbnpy-SpLa6Z0UMINKqq-mh3PF1669y3RSB-xSsWUcYaQMJcjuiL3k1TAjT0gmL4LQpxg

#2
eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Ii4rQC4rIiwibWl4cGFuZWxJZCI6IjE3YzQzYmZiNzI5MTI2NC0wYTdiYTViOGU5OTNlZi0xYzNiNjY1MC0xM2M2ODAtMTdjNDNiZmI3MmExNjQ3IiwibWl4cGFuZWxQcm9qZWN0SWQiOiI0YmZiMjQxNGFiOTczYzc0MWI2ZjA2N2JmMDZkNTU3NSIsIm9yZyI6Ii4qIiwicHViIjoibmVvNGouY29tIiwicmVnIjoiICIsInN1YiI6Im5lbzRqLWRlc2t0b3AiLCJleHAiOjE2NjU1NDI4MTUsInZlciI6IioiLCJpc3MiOiJuZW80ai5jb20iLCJuYmYiOjE2MzQwMDY4MTUsImlhdCI6MTYzNDAwNjgxNSwianRpIjoiVFV5dGh1V3VZIn0.I0CFAwnVgGKrqKcLJraDF_H5EDp3sbBn73YxvkL6UOqfVClWaSQZvR1liBffTxMHAeYUB2okCNKz1MxNRgxKKyO0se4FlhLSbhcgntbV9LRFMaZAtRwXHYCPgSQEir9K1yjW9LRQTNn6Wx9wNy1LyygCYq75VhfXIavVk6ebFo1IjjF7Rx0CMjlO4p6uw-OeRgNI1xqzTRY1Boz8BK4Fqzo7BTFIzmJuBSg_kz-j97XnrOhwK7laNychlM3w9kre2wQbEcs6hAuA09EM198DR3LtCZ_cwPr_mxoq-kfpJQ3W0SENDVzG6SyJ0xwoM_QeNgbgyWLmrbQ9ltEggXI4Lg


