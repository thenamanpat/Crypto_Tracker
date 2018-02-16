class Coin(object):
	def __init__(self, name):
		self.name = name
		self.current_position = 0
		self.current_position_average_price = ( 0 , None )
		# self.current_position_average_price_coin = None
		self.buy_orders = []
		self.sell_orders = []
		self.transfer_orders = []

		self.fee_paid = 0


