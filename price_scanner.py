import coinmarketcap
import json
from copy import deepcopy
import sys

from models import Transaction_History_Model, Price_Log_Model
from helpers import file_helper, time_converter, coin_helper


# price_entry = {
# 	"ID" : 0, 
# 	"DATE" : "", #"last_updated"
# 	"SOURCE" : "", #coinbase

# 	"SYMBOL" : "", #symbol
# 	"NAME" : "", #id
# 	"RANK" : "", #rank

# 	"PRICE_DETAILS" : {
# 		"PRICE_COIN" : "", #USD
# 		"PRICE_AMOUNT" : "", #"price_usd"

# 		"24H_VOLUME" : "", #"24h_volume_usd"
# 		"MARKET_CAP" : "" #market_cap_usd
# 	},

# 	"PERCENT_CHANGE" : {
# 		"1_HOUR" : "", #"percent_change_1h"
# 		"24_HOUR" : "", #"percent_change_24h"
# 		"7_DAY" : "" #"percent_change_7d"
# 	},

# 	"SUPPLY_DETAILS" : {
# 		"AVAILABLE_SUPPLY" : "", #"available_supply"
# 		"TOTAL_SUPPLY" : "", #"total_supply"
# 		"MAX_SUPPLY" : "" #"max_supply"
# 	}

# }

def processCoinMarketCapData(coin_data, base_dict):
	price_log = deepcopy(base_dict)

	try:
		price_log["Date".upper()] = time_converter.unix_as_datetime_str(coin_data["last_updated"])
		price_log["Source".upper()] = str("COINMARKETCAP")

		price_log["symbol".upper()] = str(coin_data["symbol"])
		price_log["name".upper()] = str(coin_data["symbol"])
		price_log["rank".upper()] = int(coin_data["rank"])


		#################

		price_log["Price_details".upper()] = {}
		price_log["Price_details".upper()]["Price_coin".upper()] = "USD"
		price_log["Price_details".upper()]["Price_amount".upper()] = float(coin_data["price_usd"])

		price_log["Price_details".upper()]["24h_volume".upper()] = float(coin_data["24h_volume_usd"])
		price_log["Price_details".upper()]["market_cap".upper()] = float(coin_data["market_cap_usd"])


		#################

		price_log["Percent_change".upper()] = {}
		price_log["Percent_change".upper()]["1_hour".upper()] = float(coin_data["percent_change_1h"])
		price_log["Percent_change".upper()]["24_hour".upper()] = float(coin_data["percent_change_24h"])
		price_log["Percent_change".upper()]["7_day".upper()] = float(coin_data["percent_change_7d"])


		#################

		price_log["Supply_details".upper()] = {}
		price_log["Supply_details".upper()]["available_supply".upper()] = float(coin_data["available_supply"])
		price_log["Supply_details".upper()]["total_supply".upper()] = float(coin_data["total_supply"])
		price_log["Supply_details".upper()]["max_supply".upper()] = float(coin_data["max_supply"])


		return (1, price_log)
	except:
		return (0, "Error while accesing CoinMarketCap Datagram")

def getCoinDetails_CoinMarketCap(coin_symbol):
	# (ret_code, coin_name) = coin_helper.CoinSymbol_Name(coin_symbol)
	# if ret_code is 0:
	# 	return (0, coin_name)

	data = coinmarketcap.getSpecificCoin("bitcoin")

	try:
		if "error" in data.keys():
			return (0, "Invalid coin access")
	except:
		return processCoinMarketCapData(coin_data=data[0], base_dict=price_entry)

def setupHeaders(price_log_head_file):
	#Coin Symbol Information 
	# coin_symbol = json.load(open('coin_symbol.json'))

	global price_entry
	global price_allowed_sources

	# #Header information
	# (ret_code, price_log_header) = file_helper.read_json_file_dict(price_log_head_file)
	# if ret_code is 0:
	# 	print "Error reading Price Log Header File"
	# 	return (0, price_log_header)

	try:
		price_log_header = Price_Log_Model.getAllData()
		price_entry = price_log_header["price_entry".upper()]
		price_allowed_sources = price_log_header["allowed_sources".upper()]

		return (1, None)

	except Exception as e:
		print "Price Log header keys are invalid"
		return (0, e)


if __name__ == "__main__":
	(ret_code, e) = setupHeaders(price_log_head_file = 'price_log_header.json')

	if ret_code is 0:
		print "Unable to setup headers"
		print e
		sys.exit()


	(ret_code, price_log) = getCoinDetails_CoinMarketCap("BTC")

	if ret_code is 1:
		(ret, (ex1, ex2)) = file_helper.append_dict_json_file(file_name='price_log.json', data=price_log)
		if (ret is 1 and ex1 is not None) or (ret is 0):
			print ex1
			print ex2
	else:
		print price_log



