
class Indicator:
	"""
Indicator class
	Technical indicator or pattern

Attributes
----------
json : dict
name : str
info : IndicatorInfo
min_threshold : MinMaxThreshold
max_threshold : MinMaxThreshold
parameters : list
	List of IndicatorParameters
raw : list
	List of raw values of technical indicator or pattern
	"""
	def __init__(self,**kwargs) -> None:
		self.json = kwargs
		self.name : str = kwargs['name']
		self.info : IndicatorInfo = IndicatorInfo(**kwargs['info'])
		self.min_threshold : MinMaxThreshold = MinMaxThreshold(**kwargs['min_threshold'])
		self.max_threshold : MinMaxThreshold = MinMaxThreshold(**kwargs['max_threshold'])
		self.parameters : list = [IndicatorParameter(**kwargs[x]) for x in kwargs.keys() if x not in ['min_threshold','max_threshold','raw','name','info']]
		self.raw : list = list(kwargs['raw'].values())

class IndicatorInfo:
	"""
IndicatorInfo
	Detailed info of technical indicator or pattern

Attributes
----------
json : dict
display_name : str
name : str
group : str
function_flags : list
input_names : dict
output_flags : dict
	"""
	def __init__(self,**kwargs) -> None:
		self.json = kwargs
		self.display_name : str = kwargs['display_name']
		self.name : str = kwargs['name']
		self.group : str = kwargs['group']
		self.function_flags : list = kwargs['function_flags']
		self.input_names : dict = kwargs['input_names']
		self.output_flags : dict = kwargs['output_flags']

class MinMaxThreshold:
	"""
MinMaxThreshold class
	Used for study code #2

Attributes
----------
json : dict
display_name : str
value : int
	Custom value to filter indicator raw values
default_value : int
	Values used if custom value is not set
help : str
	"""
	def __init__(self,**kwargs) -> None:
		self.json = kwargs
		self.display_name : str = kwargs['display_name']
		self.default_value : int = int(kwargs['default_value'])
		self.help : str = kwargs['help']
		self.value : int = kwargs['value']

class IndicatorParameter:
	"""
IndicatorParameter class

Attributes
----------
json : dict
name : str
display_name : str
help : str
type : int
	Type value of technical indicator or pattern
	values : 
		0 - float value
		2 - int value
		3 - int value
value : float or int
default_value : float or int
	"""
	def __init__(self,**kwargs) -> None:
		self.json = kwargs
		self.name : str = kwargs['name']
		self.display_name : str = kwargs['display_name']
		self.help : str = kwargs['help']
		self.type : int = int(kwargs['type'])
		if self.type == 0:
			self.default_value : float = kwargs['default_value']
			self.value : float = kwargs['value']
		elif self.type == 2 or self.type == 3:
			self.default_value : int = kwargs['default_value']
			self.value : int = kwargs['value']
