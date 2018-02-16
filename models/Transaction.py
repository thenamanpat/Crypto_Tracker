from copy import deepcopy
import datetime

class Transaction(object):
	
	transaction_entry = {
		"ID" : 0, 

		"DATE" : "", #EDT
		"TYPE" : "",

		"BUY" : "", 
		"BUY_CUR" : "",

		"SELL" : "",
		"SELL_CUR" : "",

		"FEE" : "",
		"FEE_CUR" : "",

		"EXCHANGE" : "",
		"COMMENT" : "",
	}

	vendor_list = [
		"COINBASE", 
		"BINANCE", 
		"BANK", 
		"EXTERNAL" 
	]

	allowed_types = [
	"DEPOSIT",
	"WITHDRAWAL",
	"TRADE",
	"MINING",
	"SPEND"
	]

	json_data = {
		"TRANSACTION_ENTRY" : transaction_entry,
		"VENDOR_LIST" : vendor_list, 
		"ALLOWED_TYPES" : allowed_types
	}

	def __init__(self):
		self.transaction = deepcopy(Transaction.transaction_entry)

	# def getVendorList():
	# 	return Transaction.vendor_list

	# def getAllowedTypes():
	# 	return Transaction.allowed_types

	# def getAllData():
	# 	return Transaction.json_data

	def setID(self, ID):
		self.transaction["ID"] = ID
	
	def getTransactionEntry(self):
		return self.transaction

	def getDate(self):
		return datetime.datetime.strptime(self.transaction["DATE"], '%Y-%m-%d %H:%M:%S')

	def updateTransactionData(self, date, ttype,
		buy, buy_cur, sell , sell_cur , fee , fee_cur, 
		exchange, comment):
		
		if exchange not in Transaction.vendor_list:
			return (0, "Not approved Vendor: " + exchange)

		if ttype not in Transaction.allowed_types:
			return (0, "Not approved Transaction Type: " + ttype)

		self.transaction["DATE"] = date
		self.transaction["TYPE"] = ttype

		self.transaction["BUY"] =  buy
		self.transaction["BUY_CUR"] =  buy_cur

		self.transaction["SELL"] =  sell
		self.transaction["SELL_CUR"] =  sell_cur

		self.transaction["FEE"] = fee
		self.transaction["FEE_CUR"] = fee_cur

		self.transaction["EXCHANGE"] = exchange
		self.transaction["COMMENT"] = comment

		return (1, "")


	# def newDepositTransaction( date, 
	# 	buy, buy_cur, sell , sell_cur , fee , fee_cur , 
	# 	exchange, comment):

	# 	transaction = Transaction.getNewTransactionEntry()
	# 	ttype = "DEPOSIT"
		
	# 	return updateTransactionData(date, ttype,
	# 	buy, buy_cur, sell , sell_cur , fee , fee_cur, 
	# 	exchange, comment)

	# def newWithdrawalTransaction( date, 
	# 	buy, buy_cur, sell , sell_cur , fee , fee_cur , 
	# 	exchange, comment):

	# 	ttype = "WITHDRAWAL"
		
	# 	return updateTransactionData(date, ttype, 
	# 	buy, buy_cur, sell , sell_cur , fee , fee_cur, 
	# 	exchange, comment)

	# def newTradeTransaction( date, 
	# 	buy, buy_cur, sell , sell_cur , fee , fee_cur , 
	# 	exchange, comment):

	# 	ttype = "TRADE"
		
	# 	return updateTransactionData(date, ttype, 
	# 	buy, buy_cur, sell , sell_cur , fee , fee_cur, 
	# 	exchange, comment)

	# def newMiningTransaction( date, 
	# 	buy, buy_cur, sell , sell_cur , fee , fee_cur , 
	# 	exchange, comment):

	# 	ttype = "MINING"
		
	# 	return updateTransactionData(date, ttype, 
	# 	buy, buy_cur, sell , sell_cur , fee , fee_cur, 
	# 	exchange, comment)

	# def newSpendTransaction( date, 
	# 	buy, buy_cur, sell , sell_cur , fee , fee_cur , 
	# 	exchange, comment):

	# 	ttype = "SPEND"
		
	# 	return updateTransactionData(date, ttype, 
	# 	buy, buy_cur, sell , sell_cur , fee , fee_cur, 
	# 	exchange, comment)







