# import coinmarketcap
# import json
# import currency

# import datetime

# print currency.coin_data

# data = coinmarketcap.getAllCoins()
# data = json.loads(data)
# coin_data = {}
# for item in data:
# 	coin_data[item["symbol"]] = item["id"]


# with open('coin_datain.json', 'w') as fp:
# 	json.dump(coin_data, fp)


# dates = [
# {"Date" : "2017-12-20 15:52:30", "Value" : 1},
# {"Date" : "2018-01-07 19:16:30", "Value" : 1},
# {"Date" : "2017-12-20 15:34:30", "Value" : 1},
# {"Date" : "2017-12-21 18:59:30", "Value" : 1},
# {"Date" : "2017-12-29 02:11:30", "Value" : 1},
# {"Date" : "2018-01-14 07:30:32", "Value" : 1},
# {"Date" : "2018-01-14 09:37:18", "Value" : 1}
# ]

# dates = sorted(dates, key=lambda x: datetime.datetime.strptime(x['Date'], '%Y-%m-%d %H:%M:%S'))

# # transaction_list.sort(key=lambda item:item['date'], reverse=True)
# # return sorted(transaction_list, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

# for item in dates:
# 	print item

# def minimalist_xldate_as_datetime(xldate, datemode):
#     # datemode: 0 for 1900-based, 1 for 1904-based
# 	return (
# 		datetime.datetime(1899, 12, 30)
# 		+ datetime.timedelta(days=xldate + 1462 * datemode)
# 		)


# st = minimalist_xldate_as_datetime(xldate=43109.845509259256, datemode=0)
# # print st + "Yeah"
# print str(st) + "Yeah"

# 43109.845509259256
# 2018-01-09 20:17:32
# 2018-01-09 20:17:32

# 43109.610034722224
# 2018-01-09 14:38:27

# coin_symbol = json.load(open('coin_symbol.json'))

# coin_symbol["LEND"] = "ethlend"


# with open('coin_symbol.json', 'w') as f:
# 	f.write(json.load(coin_symbol))


# import ccxt

# binance = ccxt.binance()
# markets = binance.load_markets()

# ltc_eth = binance.markets['LTC/ETH']
# neo_eth = binance.markets['NEO/ETH']

# ltc_btc = binance.markets['LTC/BTC']
# neo_btc = binance.markets['NEO/BTC']


# print ltc_btc


# print binance.id, markets


# python init.py --fresh_start 1  --transaction_history_xlsx /Users/Jiraya/Desktop/Crypto_Data/Trade_History.xlsx --program_history_dir /Users/Jiraya/Desktop/Crypto_Data --file_metadata /Users/Jiraya/Desktop/Crypto_Data/file_metadata.json



