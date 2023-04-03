"""Models module."""

__author__ = "pom11"
__copyright__ = "Copyright 2023, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "2.0.1"
__maintainer__ = "pom11"
__email__ = "office@parsecom.ro"

import typing
from importlib import import_module

if typing.TYPE_CHECKING:
	from _ohlcv import Ohlcv
	from _study import Study, StudyConfig
	from _indicator import Indicator, IndicatorInfo, IndicatorParameter, MinMaxThreshold

__all__ = [
	"Ohlcv",
	"Study",
	"StudyConfig",
	"Indicator",
	"IndicatorInfo",
	"MinMaxThreshold",
	"IndicatorParameter"
]

__cache = {}

def _build_path(string: str) -> str:
	if any(x.lower() in string.lower() for x in ['indicator','threshold']):
		return '._indicator'
	elif "study" in string.lower():
		return '._study'
	elif "ohlcv" in string.lower():
		return '._ohlcv'

def __getattr__(string):
	try:
		return __cache[string]
	except KeyError:
		pass

	if string not in __all__:
		raise ImportError(f"Package 'sphoin.models' has no class '{string}'")

	module = import_module(_build_path(string), package="sphoin.models")
	class__ = getattr(module, string)

	__cache[string] = class__
	return class__