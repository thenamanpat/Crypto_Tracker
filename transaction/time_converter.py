import datetime

def xldate_as_datetime_str(xldate):
	return str(
		datetime.datetime(1899, 12, 30) + 
		datetime.timedelta(days=xldate)
		)

def unix_as_datetime_str(unix_stamp):
	return datetime.datetime.fromtimestamp(int(unix_stamp)).strftime('%Y-%m-%d %H:%M:%S')