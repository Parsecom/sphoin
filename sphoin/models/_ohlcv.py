class Ohlcv:
	"""
Ohlcv class

Attributes
----------
json : dict
date : list
	List of dates
open : list
	List of open values
high : list
	List of high values
low : list
	List of low values	
close : list
	List of close values
volume : list
	List of volume values
	"""
	def __init__(self,**kwargs) -> None:
		self.json = kwargs
		self.date : list = kwargs['date']
		self.open : list = kwargs['open']
		self.high : list = kwargs['high']
		self.low : list = kwargs['low']
		self.close : list = kwargs['close']
		self.volume : list = kwargs['volume']
