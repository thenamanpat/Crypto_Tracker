import sys
sys.path.append('/..')

from api import coinmarketcap
from helpers import file_helper
import json


def CoinSymbol_Name(coin_symbol):
	(ret_code, price_log_header) = file_helper.read_json_file_dict(file_name="coin_symbol.json")

	return (1, 'bitcoin')

def CoinName_Symbol(coin_name):
	pass

def buildCoinSymbolMap():
	data = coinmarketcap.getAllCoins()

	to_return = {}

	for item in data:
		to_return[item["symbol"]] = dict(item)
		to_return[item["id"]] = str(item["symbol"])
	
	return file_helper.write_dict_json_file(file_name="coin_symbol.json", data=to_return)



if __name__ == "__main__":
	buildCoinSymbolMap()
	pass