from copy import deepcopy

class TransactionHistory_Model(object):

	transaction_entry = {
		"ID" : 0, 
		"DATE" : "", #EDT
		"TYPE" : "",

		"PRICE_DETAILS" : {
			"PRICE COIN" : "",
			"PRICE" : 0,
		},

		"FEE_DETAILS" : {
			"FEE_COIN" : "",
			"FEE_AMOUNT" : 0,
		},

		"COIN_DETAILS" : {
			#For Type TRANSFER
			"COIN" : "",
			"AMOUNT" : 0,
			#####################

			#For Type EXCHANGE
			"SOURCE_COIN" : "",
			"SOURCE_AMOUNT" : 0,

			"TARGET_COIN" : "",
			"TARGET_AMOUNT" : 0,
			############################
		},

		"PLATFORM_DETAILS" : {
			#For Type TRANSFER
			"SOURCE_VENDOR" : "",
			"TARGET_VENDOR" : "",
			####################

			#For Type EXCHANGE
			"EXCHANGE" : "",
			##################
		}
	}

	vendor_list = [
		"COINBASE", 
		"BINANCE", 
		"BANK", 
		"EXTERNAL" 
	]

	allowed_types = { 
		"0": "EXCHANGE" , 
		"1" : "TRANSFER" 
	}

	json_data = {
		"TRANSACTION_ENTRY" : transaction_entry,
		"VENDOR_LIST" : vendor_list, 
		"ALLOWED_TYPES" : allowed_types
	}

	def __init__(self):
		self.transaction = deepcopy(TransactionHistory_Model.transaction_entry)

	def getTransactionEntry(self):
		return self.transaction

	def getVendorList(self):
		return TransactionHistory_Model.vendor_list

	def getAllowedTypes(self):
		return TransactionHistory_Model.allowed_types

	def getAllData(self):
		return TransactionHistory_Model.json_data

# if __name__ == "__main__":
# 	file_helper.write_dict_json_file(file_name='./headers/transaction_history_header.json', data=json_data)
