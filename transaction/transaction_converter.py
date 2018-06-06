import time_converter

#TRANSFER = "Date	Source	Target	Coin	Price	Amount	Total	Total Coin	Fee	Fee/ Coin Type"
def processTransferTransaction(source_header, row_values, base_model):
	try:

		source_vendor = str(row_values[source_header.index("SOURCE")]).upper()
		dest_vendor = str(row_values[source_header.index("TARGET")]).upper()

		source_amount = float(row_values[source_header.index("AMOUNT")])
		fee_amount = float(row_values[source_header.index("FEE")])
		dest_amount = source_amount - fee_amount

		coin_name = str(row_values[source_header.index("COIN".upper())])

		transaction_deposit = base_model.getTransactionEntry()
		(ret_code, ret_message) = transaction_deposit.newDepositTransaction(self, 
			date = time_converter.xldate_as_datetime_str(row_values[source_header.index("DATE")]),
			buy = source_amount, 
			buy_cur = coin_name, 
			sell = None, 
			sell_cur = None, 
			fee = None, 
			fee_cur = None, 
			exchange = dest_vendor, 
			comment = None)

		if ret_code == 0:
			return (ret_code, ret_message)


		transaction_withdraw = base_model.getTransactionEntry()
		(ret_code, ret_message) = transaction.newWithdrawalTransaction(self, 
			date = time_converter.xldate_as_datetime_str(row_values[source_header.index("DATE")]),
			buy = None, 
			buy_cur = None, 
			sell = dest_amount, 
			sell_cur = coin_name, 
			fee = fee_amount, 
			fee_cur = coin_name, 
			exchange = source_vendor, 
			comment = None)

		if ret_code == 0:
			return (ret_code, ret_message)
		
		return (1 , (transaction_deposit , transaction_withdraw))

	except Exception as e:
		return (0, e)

def sortTransactionList(transaction_list):
	to_return = sorted(transaction_list, 
		key=lambda x: x.getDate())

	# counter = 0

	# for i in range(len(to_return)):
	# 	to_return[i].setID(counter)
	# 	counter += 1

	return to_return

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







