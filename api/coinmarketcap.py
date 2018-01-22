import requests
import json

def getAllCoins():
	r = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=0")
	return json.loads(r.content)

def getSpecificCoin(coin):
	r = requests.get("https://api.coinmarketcap.com/v1/ticker/" + coin)
	return json.loads(r.content)


# coinmarketcap = Market()
# # coinmarketcap.ticker(<currency>, limit=3, convert='EUR')

# data = coinmarketcap.ticker()
# json_data = json.loads(data)

# with open('coin_data.txt', 'w') as outfile:
# 	json.dump(json_data, outfile)

