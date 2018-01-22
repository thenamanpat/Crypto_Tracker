

# file_metadata = {
# 	transaction_history_source_xlsx = [ "" ],
# 	data_store_dir_path = [ "" ],
# 	current_holding_path = [ "" ],
# 	price_history_path = [ "" ]
# }

from copy import deepcopy


class File_DB(object):
	TRANS_HIST_KEY = "transaction_history_source_xlsx".upper()
	DATA_DIR_KEY = "data_store_dir_path".upper()

	HOLDING_LEDGER_FILE_NAME = "current_holdings.json"
	PRICE_HISTORY_FILE_NAME = "price_history.json"
	TRANS_HIST_FILE_NAME = "transaction_history.json"

	def __init__(self, file_metadata_path=None, file_metadata=None, 
		transaction_history_xlsx=None, program_history_dir=None):
		
		self.file_metadata_path = file_metadata_path

		if file_metadata is None:
			self.file_metadata = {}
			self.file_metadata[File_DB.TRANS_HIST_KEY] = transaction_history_xlsx
			self.file_metadata[File_DB.DATA_DIR_KEY] = program_history_dir
		else:
			self.file_metadata = deepcopy(file_metadata)

	def getCurrentHoldingFile(self):
		return (self.file_metadata[File_DB.DATA_DIR_KEY] + "/" + File_DB.HOLDING_LEDGER_FILE_NAME)

	def getPriceHistoryFile(self):
		return (self.file_metadata[File_DB.DATA_DIR_KEY] + "/" + File_DB.PRICE_HISTORY_FILE_NAME)

	def getTransactionHistoryFile(self):
		return (self.file_metadata[File_DB.DATA_DIR_KEY] + "/" + File_DB.TRANS_HIST_FILE_NAME)

	def getTransactionHistory_Xlsx(self):
		return self.file_metadata[File_DB.TRANS_HIST_KEY]

	def getFileDatagram(self):
		return self.file_metadata

	def getAllDataFiles(self):
		return [self.getCurrentHoldingFile() , self.getPriceHistoryFile(), self.getTransactionHistoryFile()]



	def setDataDir(self, program_history_dir):
		self.file_metadata[File_DB.DATA_DIR_KEY] = program_history_dir

	def setTransHist(self, transaction_history_xlsx):
		self.file_metadata[File_DB.TRANS_HIST_KEY] = transaction_history_xlsx





