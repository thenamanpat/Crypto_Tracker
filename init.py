import argparse
import simplejson as json
import datetime 
import sys
import xlrd
from copy import deepcopy

from models.File_DB import File_DB
from models.TransactionHistory_Model import TransactionHistory_Model
from models.PriceLog_Model import PriceLog_Model

from helpers import file_helper, time_converter, xlsx_to_json_parser


def getFileSystem(args):
	if (args.fresh_start):
		print "Deleting all previous history of data. Time for a fresh start."
		
		if (args.file_metadata):
			(ret_code, file_metadata) = file_helper.clear_dict_json_file(file_name=args.file_metadata)
			
			if ret_code is 0:
				return (0, file_metadata)
		else:
			return (0, "PLease specify the file for storing file metadata")

		to_return = File_DB(file_metadata_path=args.file_metadata)

		if (args.transaction_history_xlsx):
			to_return.setTransHist(args.transaction_history_xlsx)
		else:
			return (0, "PLease specify the file for Transaction History")

		if (args.program_history_dir):
			to_return.setDataDir(args.program_history_dir)

			for file_to_check in to_return.getAllDataFiles():
				(ret_code , e) = file_helper.clear_dict_json_file(file_name=file_to_check)
				
				if ret_code is 0:
					return (0, e)

		else:
			return (0, "PLease specify the Directory for storing Program Data")


		(ret_code, file_metadata) = file_helper.write_dict_json_file(file_name=args.file_metadata, 
			data=to_return.getFileDatagram())
		
		if ret_code is 0:
			return (0, file_metadata)

		return (1, to_return)
	
	if (args.file_metadata):
		(ret_code, file_metadata) = file_helper.read_json_file_dict(file_name=args.file_metadata)
		if ret_code is 0:
			print "Error while parsing metadata file"
			return (0, file_metadata)

		to_return = File_DB(file_metadata_path=args.file_metadata, file_metadata=file_metadata)
		return (1, to_return)

	return (0, "Not enough arguments provided for File System setup")


def readTransactionHistory(file_database, base_model):
	transaction_list = []

	transaction_workbook = xlrd.open_workbook(file_database.getTransactionHistory_Xlsx())
	sheetNames = transaction_workbook.sheet_names()

	for (index,sheet_name) in enumerate(sheetNames):
		sheet_data = transaction_workbook.sheet_by_index(index)
		sheet_header = [str(x).upper() for x in sheet_data.row_values(0)]

		(ret_code, transactions) = xlsx_to_json_parser.processTransactionSheet(
			source_header = sheet_header,
			source_sheet = sheet_data, 
			vendor = sheet_name.upper(),
			base_model=base_model)

		if ret_code is 0:
			return (0 , transactions)
		else:
			transaction_list.extend(transactions)

	#Sort transaction_list based on Date
	transaction_list = xlsx_to_json_parser.sortTransactionList(
		transaction_list = transaction_list, 
		field = "Date".upper())

	return (1, transaction_list)

	# (ret_code, ex) = file_helper.write_dict_json_file(file_name='transaction_history.json', data=transaction_list)

	# if ret_code is 0:
	# 	print "Error while writing file"
	# 	print ex

def findNewTransactions(file_database, transaction_list):
	(ret_code, current_list) = file_helper.read_json_file_dict(file_name=file_database.getTransactionHistoryFile())

	if ret_code is 0:
		return (0, current_list)

	# print len(transaction_list)
	print len(current_list)

	if len(transaction_list) > len(current_list):
		# New Transactions have been added
		return (1, transaction_list[len(current_list):])

	return (1, None)

def setupHeaders():
	global transaction_entry
	global transaction_vendor_list
	global transaction_allowed_types

	try:
		transaction_header = Transaction_History_Model.getAllData()
		transaction_entry = transaction_header["transaction_entry".upper()]
		transaction_vendor_list = transaction_header["vendor_list".upper()]
		transaction_allowed_types = transaction_header["allowed_types".upper()]

		return (1, None)

	except Exception as e:
		print "Transaction header keys are invalid"
		return (0, e)


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("--file_metadata", help="File Path for location of file paths. Created during setup.")
	parser.add_argument("--fresh_start", help="Will ignore all previous program data files. Will go over all transactions again to create current ledger.")
	parser.add_argument("--transaction_history_xlsx", help="File Path for location of Transaction History file in xlsx format.")
	parser.add_argument("--program_history_dir", help="Directory Path for location where program will store data.")
	args = parser.parse_args()

	(ret_code, file_database) = getFileSystem(args)

	if ret_code is 0:
		print file_database
		sys.exit(0)

	print file_database.getFileDatagram()

	(ret_code, transaction_list) = readTransactionHistory(file_database=file_database, base_model=TransactionHistory_Model())

	if ret_code is 0:
		print "Error while reading Transaction History Xlsx File"
		print transaction_list

	# print transaction_list

	(ret_code, new_transactions) = findNewTransactions(file_database=file_database, transaction_list=transaction_list)
	if ret_code is 0:
		print "Error while reading Program data transaction history"
		print new_transactions

	print new_transactions



	



