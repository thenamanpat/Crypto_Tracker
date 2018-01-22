from copy import deepcopy

class PriceLog_Model(object):
	price_entry = {
		"ID" : 0, 
		"DATE" : "", 
		"SOURCE" : "", 

		"SYMBOL" : "", 
		"NAME" : "", 
		"RANK" : "", 

		"PRICE_DETAILS" : {
			"PRICE_COIN" : "", 
			"PRICE_AMOUNT" : "", 

			"24H_VOLUME" : "", 
			"MARKET_CAP" : "" 
		},

		"PERCENT_CHANGE" : {
			"1_HOUR" : "", 
			"24_HOUR" : "", 
			"7_DAY" : "" 
		},

		"SUPPLY_DETAILS" : {
			"AVAILABLE_SUPPLY" : "", 
			"TOTAL_SUPPLY" : "", 
			"MAX_SUPPLY" : "" 
		}

	}

	allowed_sources = [
		"COINBASE",
		"COINMARKETCAP",
		"BINANCE",  
		"OTHER" 
	]

	json_data = {
		"PRICE_ENTRY" : price_entry,
		"ALLOWED_SOURCES" : allowed_sources
	}


	def __init__(self):
		self.entry = deepcopy(PriceLog_Model.price_entry)

	def getPriceEntry(self):
		return self.entry

	def getAllowedSources(self):
		return PriceLog_Model.allowed_sources

	def getAllData(self):
		return PriceLog_Model.json_data


# if __name__ == "__main__":
# 	file_helper.write_dict_json_file(file_name='price_log_header.json', data=json_data)

