import simplejson as json


def read_json_file_dict(file_name):
	try:
		return (1, json.load(open(file_name)))
	except Exception as e:
		return (0, e)


def write_dict_json_file(file_name, data):
	try:
		j = json.dumps(data)

		with open(file_name, 'w') as f:
			f.write(j)

		return (1, None)
	except Exception as e:
		return (0, e)

def clear_dict_json_file(file_name):
	# try:
	# 	j = json.dumps([])

	# 	with open(file_name, 'w') as f:
	# 		f.write(j)
	# 	return (1, None)
	# except Exception as e:
	# 	return (0, e)

	return write_dict_json_file(file_name=file_name, data=[])

def append_dict_json_file(file_name, data):
	try:
		data_history = json.load(open(file_name))
		data_history.append(data)

		j = json.dumps(data_history)

		with open(file_name, 'w') as f:
			f.write(j)
		return (1, (None,None))
	
	except Exception as e:
		
		try:
			j = json.dumps([data])

			with open(file_name, 'w') as f:
				f.write(j)
			return (1, ("File does not exist. Making new one", e))
		
		except Exception as e1:
			return (0, (e,e1))


