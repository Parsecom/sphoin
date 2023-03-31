from ._indicator import Indicator

class Study:
	"""
Study class

Attributes
----------
crt : str
	Study index number
name : str
	Study custom name
study : str
	Study name
	['U|D','M|M','X','---','[ ]']
description : str
	Study description
code : str
	Study code
	['#1','#2','#3','#4','#5']
normalize : bool
	True if values are normalized and False if not
inverse : bool
	True if resulting signals are inversed and False is not
config : dict
	StudyConfig
result : list
	List of resulted signals
	"""
	def __init__(self,**kwargs) -> None:
		self.json = kwargs
		self.crt : str = kwargs['crt']
		self.name : str = kwargs['name']
		self.study : str = kwargs['study']
		self.code : str = kwargs['code']
		self.description : str = kwargs['description']
		self.normalize : bool = kwargs['normalize']
		self.inverse : bool = kwargs['inverse']
		self.config : dict = StudyConfig(**kwargs['config'])
		self.result : list = list(kwargs['result'].values())

class StudyConfig:
	"""
StudyConfig class

Attributes
----------
indicator_1: Indicator
indicator_2: Indicator
	None: If the Study uses only 1 technical indicator or pattern
	"""
	def __init__(self,**kwargs) -> None:
		self.json = kwargs
		self.indicator_1 : Indicator = None
		self.indicator_2 : Indicator = None
		for x in kwargs.keys():
			if x not in ['raw','PASSS']:
				if self.indicator_1 == None:
					data = kwargs[x]
					data['name'] = x
					data['raw'] = kwargs['raw'][x]
					self.indicator_1 : Indicator = Indicator(**data)
				elif self.indicator_2 == None:
					data = kwargs[x]
					data['name'] = x
					data['raw'] = kwargs['raw'][x]
					self.indicator_2 : Indicator = Indicator(**data)
			elif x == 'PASSS':
				self.indicator_2 : Indicator = None