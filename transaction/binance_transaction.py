import time_converter
import transaction_converter
import xlrd

def marketFieldExtractor(input_market):
	# Return (last 3, rem. first)
	return (input_market[-3:], input_market[:-3])

#source_header = "Date	Market	Type	Price	Amount	Total	Fee	Fee/ Coin"
def processTradeTransaction(source_header, row_values, vendor, base_model):
	# try:
	# Return (last 3, rem. first)
	input_market = marketFieldExtractor(row_values[source_header.index("MARKET")])
	if input_market is None:
		return (0, "Unkown Market Name")

	source_coin = 0
	dest_coin = 0
	source_amount = 0
	dest_aount = 0


	input_type = str(row_values[source_header.index("TYPE")]).upper()

	if ( input_type == str("BUY") ): #BUY 
		#If input type is BUY 
		#source_coin = last 3
		#Source_Amount = TOTAL

		#dest_coin = first
		#dest_amount = AMOUNT

		(source_coin, dest_coin) = input_market

		source_amount = float(row_values[source_header.index("TOTAL")])
		dest_aount = float(row_values[source_header.index("AMOUNT")])

	elif ( input_type == str("SELL") ): #SELL
		#If input type is SELL 
		#source_coin = first
		#Source_Amount = AMOUNT

		#dest_coin = last 3
		#dest_amount = TOTAL
		(dest_coin , source_coin) = input_market

		source_amount = float(row_values[source_header.index("AMOUNT")])
		dest_aount = float(row_values[source_header.index("TOTAL")])
	
	else:
		return (0, "Unkown Transaction Type")
	 
	####### #######
	transaction = base_model()
	(ret_code, ret_message) = transaction.updateTransactionData( 
		date = time_converter.xldate_as_datetime_str(row_values[source_header.index("Date".upper())]), 
		ttype = "TRADE",
		buy = float(source_amount), 
		buy_cur = str(source_coin).upper(), 
		sell = float(dest_aount), 
		sell_cur = str(dest_coin).upper(), 
		fee = float(row_values[source_header.index("FEE")]), 
		fee_cur = str(row_values[source_header.index("FEE COIN")]).upper(), 
		exchange = str(vendor.upper()), 
		comment = None)

	if ret_code == 0:
		return (ret_code, ret_message)

	# print transaction.transaction

	return (1 , transaction)
	
	# except Exception as e:
	# 	raise e
		# return (0, e)

#deposit = "Date	Coin	Amount	Address	TXID	Status"
def processDepositTransaction(source_header, row_values, vendor, base_model):
	# try:
	transaction = base_model()
	(ret_code, ret_message) = transaction.updateTransactionData(
		date = time_converter.xldate_as_datetime_str(row_values[source_header.index("DATE")]),
		ttype = "DEPOSIT",
		buy = float(row_values[source_header.index("AMOUNT")]), 
		buy_cur = str(row_values[source_header.index("COIN")]), 
		sell = None, 
		sell_cur = None, 
		fee = None, 
		fee_cur = None, 
		exchange = vendor, 
		comment = None)

	if ret_code == 0:
		return (ret_code, ret_message)
	
	return (1 , transaction)

	# except Exception as e:
	# 	# return (0, e)
	# 	raise e

#deposit = "Date	Coin	Amount	Address	TXID	Status"
def processWithdrawalTransaction(source_header, row_values, vendor, base_model):
	# try:

	dest_amount = float(row_values[source_header.index("AMOUNT")])
	coin_name = str(row_values[source_header.index("COIN".upper())])

	transaction = base_model()
	(ret_code, ret_message) = transaction.updateTransactionData( 
		date = time_converter.xldate_as_datetime_str(row_values[source_header.index("DATE")]),
		ttype = "WITHDRAWAL",
		buy = None, 
		buy_cur = None, 
		sell = dest_amount, 
		sell_cur = coin_name, 
		fee = None, 
		fee_cur = None, 
		exchange = vendor, 
		comment = None)

	if ret_code == 0:
		return (ret_code, ret_message)
	
	return (1 , transaction)

	# except Exception as e:
	# 	# return (0, e)
	# 	raise e

def processTransactionSheet(sheet_name, source_header, source_sheet, vendor, base_model):
	transaction_list = []

	# try:
	if "TRADE" == sheet_name:
		for rownum in range(1, source_sheet.nrows):
			row_values = source_sheet.row_values(rownum)
			
			(ret_code, transactions) = processTradeTransaction(
				source_header = source_header,
				row_values = row_values, 
				vendor = "BINANCE",
				base_model=base_model)

			if ret_code is 0:
				return (0 , transactions)
			else:
				transaction_list.append(transactions)

	elif "DEPOSIT" == sheet_name:
		for rownum in range(1, source_sheet.nrows):
			row_values = source_sheet.row_values(rownum)

			(ret_code, transactions) = processDepositTransaction(
				source_header = source_header,
				row_values = row_values, 
				vendor = "BINANCE",
				base_model=base_model)

			if ret_code is 0:
				return (0 , transactions)
			else:
				transaction_list.append(transactions)

	elif "WITHDRAWAL" == sheet_name:
		for rownum in range(1, source_sheet.nrows):
			row_values = source_sheet.row_values(rownum)

			(ret_code, transactions) = processWithdrawalTransaction(
					source_header = source_header,
					row_values = row_values, 
					vendor = "BINANCE",
					base_model=base_model)

			if ret_code is 0:
				return (0 , transactions)
			else:
				transaction_list.append(transactions)

	else:
		return (0, "The Sheet Name " + sheet_name + " was not recognized")

	return (1, transaction_list)

	# except Exception as e:
	# 	# return (0, e)
	# 	raise e

def readTransactionHistory(xlsx_file_name, base_model):
	transaction_list = []

	transaction_workbook = xlrd.open_workbook(xlsx_file_name)
	sheetNames = [str(x).upper() for x in transaction_workbook.sheet_names()]
	
	# Trade # Deposit # WITHDRAWAL
	for (index,sheet_name) in enumerate(sheetNames):
		sheet_data = transaction_workbook.sheet_by_index(index)
		sheet_header = [str(x).upper() for x in sheet_data.row_values(0)]

		(ret_code, transactions) = processTransactionSheet(sheet_name , sheet_header, sheet_data, "Binance", base_model)
		
		if ret_code is 0:
			return (0, ret_code)

		transaction_list.extend(transactions)

	# print transaction_list
	#Sort transaction_list based on Date
	# print base_model.getAllowedTypes()
	transaction_list = transaction_converter.sortTransactionList(
		transaction_list = transaction_list)

	return (1, transaction_list)