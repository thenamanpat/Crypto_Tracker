import xlrd
import simplejson as json
import datetime 
import sys
# from copy import deepcopy

# from models import Transaction_History_Model, Price_Log_Model
import time_converter

def marketFieldExtractor(input_market):
	# Return (last 3, rem. first)
	return (input_market[-3:], input_market[:-3])

# def marketFieldExtractor(input_market):
# 	for cur_len in range(3, len(input_market)):
# 		last = input_market[-cur_len:]
# 		first = input_market[:-cur_len]

# 		print last,first

# 		if (first in coin_symbol.keys()) and (last in coin_symbol.keys()):
# 			# Return (last , rem. first)
# 			return (last,first)

# 	# Return (last 3, rem. first)
# 	# return (input_market[-3:], input_market[:-3])
# 	return None

# def xldate_as_datetime_str(xldate):
# 	return str(
# 		datetime.datetime(1899, 12, 30) + 
# 		datetime.timedelta(days=xldate)
# 		)

#TRANSFER = "Date	Source	Target	Coin	Price	Amount	Total	Total Coin	Fee	Fee/ Coin Type"
def processTransferTransaction(source_header, row_values, base_model):
	transaction = base_model.getTransactionEntry()
	transaction_vendor_list = base_model.getVendorList()
	transaction_allowed_types = base_model.getAllowedTypes()

	source_vendor = str(row_values[source_header.index("Source".upper())]).upper()
	dest_vendor = str(row_values[source_header.index("Target".upper())]).upper()

	if (source_vendor not in transaction_vendor_list) or (dest_vendor not in transaction_vendor_list):
		return (0, "Not approved Vendor")

	try:
		transaction["Date".upper()] = time_converter.xldate_as_datetime_str(row_values[source_header.index("Date".upper())])
		transaction["Type".upper()] = str(transaction_allowed_types["1"])

		###############

		transaction["Price_details".upper()] = {}

		transaction["Price_details".upper()]["Price coin".upper()] = str(row_values[source_header.index("Total Coin".upper())])

		transaction["Price_details".upper()]["Price".upper()] = float(row_values[source_header.index("Price".upper())])

		###############

		transaction["Fee_details".upper()] = {}

		transaction["Fee_details".upper()]["Fee_Coin".upper()] = str(row_values[source_header.index("Fee Coin".upper())])

		transaction["Fee_details".upper()]["Fee_Amount".upper()] = float(row_values[source_header.index("Fee".upper())])

		###############
		
		transaction["Coin_details".upper()] = {}

		transaction["Coin_details".upper()]["Coin".upper()] = str(row_values[source_header.index("Coin".upper())])

		transaction["Coin_details".upper()]["Amount".upper()] = float(row_values[source_header.index("Amount".upper())])

		###############

		
		transaction["Platform_details".upper()] = {}
		transaction["Platform_details".upper()]["Source_Vendor".upper()] = source_vendor
		transaction["Platform_details".upper()]["Target_Vendor".upper()] = dest_vendor
		
		return (1 , transaction)

	except Exception as e:
		return (0, e)

#TRADE = "Date	Market	Type	Price	Amount	Total	Fee	Fee/ Coin"
def processTradeTransaction(source_header, row_values, vendor, base_model):
	transaction = base_model.getTransactionEntry()
	transaction_vendor_list = base_model.getVendorList()
	transaction_allowed_types = base_model.getAllowedTypes()

	if (vendor.upper() not in transaction_vendor_list):
		return (0, "Not approved Vendor")

	try:
		# Return (last 3, rem. first)
		input_market = marketFieldExtractor(row_values[source_header.index("Market".upper())])
		if input_market is None:
			return (0, "Unkown Market Name")

		source_coin = 0
		dest_coin = 0
		source_amount = 0
		dest_aount = 0


		input_type = str(row_values[source_header.index("Type".upper())]).upper()

		if ( input_type == str("BUY") ): #BUY 
			#If input type is BUY 
			#source_coin = last 3
			#Source_Amount = TOTAL

			#dest_coin = first
			#dest_amount = AMOUNT

			(source_coin, dest_coin) = input_market

			source_amount = float(row_values[source_header.index("Total".upper())])
			dest_aount = float(row_values[source_header.index("Amount".upper())])

		elif ( input_type == str("SELL") ): #SELL
			#If input type is SELL 
			#source_coin = first
			#Source_Amount = AMOUNT

			#dest_coin = last 3
			#dest_amount = TOTAL
			(dest_coin , source_coin) = input_market

			source_amount = float(row_values[source_header.index("Amount".upper())])
			dest_aount = float(row_values[source_header.index("Total".upper())])
		
		else:
			return (0, "Unkown Transaction Type")
		 
		####### TRADE
		transaction["Date".upper()] = time_converter.xldate_as_datetime_str(row_values[source_header.index("Date".upper())])
		transaction["Type".upper()] = str(transaction_allowed_types["0"])



		###############

		transaction["Price_details".upper()] = {}

		transaction["Price_details".upper()]["Price Coin".upper()] = str(source_coin).upper()

		transaction["Price_details".upper()]["Price".upper()] = float(row_values[source_header.index("Price".upper())])

		###############

		transaction["Coin_details".upper()] = {}

		transaction["Coin_details".upper()]["Source_Coin".upper()] =  str(source_coin).upper()
		transaction["Coin_details".upper()]["Source_Amount".upper()] =  float(source_amount)

		transaction["Coin_details".upper()]["Target_Coin".upper()] =  str(dest_coin).upper()
		transaction["Coin_details".upper()]["Target_Amount".upper()] =  float(dest_aount)


		###############

		transaction["Fee_details".upper()] = {}

		transaction["Fee_details".upper()]["Fee_Coin".upper()] = str(row_values[source_header.index("Fee Coin".upper())]).upper()

		transaction["Fee_details".upper()]["Fee_Amount".upper()] = float(row_values[source_header.index("Fee".upper())])

		###############

		transaction["Platform_details".upper()] = {}
		transaction["Platform_details".upper()]["Exchange".upper()] = str(vendor.upper())


		return (1 , transaction)
	
	except Exception as e:
		return (0, e)

# transaction_entry = {
# 	"ID" : 0, 
# 	"DATE" : "",
# 	"TYPE" : "",

# 	"PRICE_DETAILS" : {
# 		"PRICE COIN" : "",
# 		"PRICE" : 0,
# 	},

# 	"FEE_DETAILS" : {
# 		"FEE_COIN" : "",
# 		"FEE_AMOUNT" : 0,
# 	},

# 	"COIN_DETAILS" : {
# 		#For Type TRANSFER
# 		"COIN" : "",
# 		"AMOUNT" : 0,
# 		#####################

# 		#For Type EXCHANGE
# 		"SOURCE_COIN" : "",
# 		"SOURCE_AMOUNT" : 0,

# 		"TARGET_COIN" : "",
# 		"TARGET_AMOUNT" : 0,
# 		############################
# 	},

# 	"PLATFORM_DETAILS" : {
# 		#For Type TRANSFER
# 		"SOURCE_VENDOR" : "",
# 		"TARGET_VENDOR" : "",
# 		####################

# 		#For Type EXCHANGE
# 		"EXCHANGE" : "",
# 		##################
# 	}
# }

def processTransactionSheet(source_header, source_sheet, vendor, base_model):

	transaction_list = []

	try:
		for rownum in range(1, source_sheet.nrows):
			row_values = source_sheet.row_values(rownum)

			input_type = str(row_values[source_header.index("Type".upper())]).upper()

			if ( input_type == str("TRANSFER") ): #TRANSFER
				(ret_code, transaction) = (processTransferTransaction(
					source_header=source_header, 
					row_values=row_values,
					base_model=base_model))

				if ret_code == 0:
					return (0, transaction)
			
			else:
				(ret_code, transaction) = (processTradeTransaction(
					source_header=source_header, 
					row_values=row_values, 
					vendor=vendor,
					base_model=base_model))

				if ret_code == 0:
					return (0, transaction)


			transaction_list.append(transaction)

		return (1 , transaction_list)

	except Exception as e:
		return (0, e)


def sortTransactionList(transaction_list, field):
	to_return = sorted(transaction_list, 
		key=lambda x: datetime.datetime.strptime(x[field.upper()], '%Y-%m-%d %H:%M:%S'))

	counter = 0

	for i in range(len(to_return)):
		to_return[i]["ID".upper()] = counter
		counter += 1

	return to_return

# def setupHeaders():
# 	global transaction_entry
# 	global transaction_vendor_list
# 	global transaction_allowed_types

# 	try:
# 		transaction_header = Transaction_History_Model.getAllData()
# 		transaction_entry = transaction_header["transaction_entry".upper()]
# 		transaction_vendor_list = transaction_header["vendor_list".upper()]
# 		transaction_allowed_types = transaction_header["allowed_types".upper()]

# 		return (1, None)

# 	except Exception as e:
# 		print "Transaction header keys are invalid"
# 		return (0, e)

# if __name__ == "__main__":

# 	(ret_code, e) = setupHeaders()

# 	if ret_code is 0:
# 		print "Unable to setup headers"
# 		print e
# 		sys.exit()

# 	wb = xlrd.open_workbook('data/Trade_History.xlsx')

# 	binance_history = wb.sheet_by_index(0)
# 	coinbase_history = wb.sheet_by_index(1)
# 	transfer_history = wb.sheet_by_index(2)


# 	binance_xl_header = [str(x).upper() for x in binance_history.row_values(0)]
# 	coinbase_xl_header = [str(x).upper() for x in coinbase_history.row_values(0)]
# 	transfer_xl_header = [str(x).upper() for x in transfer_history.row_values(0)]

# 	transaction_list = []
# 	base_dict = transaction_entry

# 	# Evaluate Transactions of binance
# 	(ret_code, trans) = processTransactionSheet(
# 		source_header = binance_xl_header,
# 		source_sheet = binance_history, 
# 		vendor = "BINANCE",
# 		base_dict=base_dict)

# 	if ret_code is 0:
# 		print "Error while parsing Biance history."
# 		print trans
# 	else:
# 		transaction_list.extend(trans)

# 	# Evaluate Transactions of coinbase
# 	(ret_code, trans) = processTransactionSheet(
# 		source_header = coinbase_xl_header,
# 		source_sheet = coinbase_history, 
# 		vendor = "COINBASE",
# 		base_dict=base_dict)

# 	if ret_code is 0:
# 		print "Error while parsing Coinbase history"
# 		print trans
# 	else:
# 		transaction_list.extend(trans)

# 	# Evaluate Transfers
# 	(ret_code, trans) = processTransactionSheet(
# 		source_header = transfer_xl_header,
# 		source_sheet = transfer_history,
# 		vendor = None,
# 		base_dict=base_dict) 

# 	if ret_code is 0:
# 		print "Error while parsing Transfer history"
# 		print trans
# 	else:
# 		transaction_list.extend(trans)

# 	#Sort transaction_list based on Date
# 	transaction_list = sortTransactionList(
# 		transaction_list = transaction_list, 
# 		field = "Date".upper())

# 	(ret_code, ex) = file_helper.write_dict_json_file(file_name='transaction_history.json', data=transaction_list)

# 	if ret_code is 0:
# 		print "Error while writing file"
# 		print ex

