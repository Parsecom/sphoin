"""Plot module."""

__author__ = "pom11"
__copyright__ = "Copyright 2023, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "2.0.7"
__maintainer__ = "pom11"
__email__ = "office@parsecom.ro"

import typing
from importlib import import_module
from rich.text import Text

if typing.TYPE_CHECKING:
	from ._plot import Plot
	from ._utils import isNumber, uni_chars, intersperse

__all__ = [
	"Plot"
]

__cache = {}

def _build_path(string: str) -> str:
	if "plot" in string.lower():
		return '._plot'
	elif any(x.lower() in string.lower() for x in ['isNumber','uni_chars','text_with_style']):
		return '._utils'

def __getattr__(string):
	try:
		return __cache[string]
	except KeyError:
		pass

	if string not in __all__:
		raise ImportError(f"Package 'sphoin.plot' has no class '{string}'")

	module = import_module(_build_path(string), package="sphoin.plot")
	class__ = getattr(module, string)

	__cache[string] = class__
	return class__

def intersperse(_list: list, item):
	result = [item] * (len(_list) * 2 -1)
	result[0::2] = _list
	return result


def test():

	from ..app import Slot
	from ._plot import Plot
	from rich.console import Console

	console = Console()

	slot = Slot(config='example')

	close = Plot.line(
		series=slot.ohlcv.close,
		signals=slot.signals_sum,
		min_flag=slot.min_flag,
		max_flag=slot.max_flag, 
		color1=slot.colors['1'], 
		color2=slot.colors['-1'],
		sizeX=console.size.width,
		sizeY=20,
		signal_as_line=True,
		dark_theme=False,
		brightness=False)
	console.print(close)

	time = Plot.time_bar(slot=slot,sizeX=console.size.width,dark_theme=False)
	console.print(time)

	signals = Plot.line(
		series=slot.signals_sum,
		signals=slot.signals_sum,
		min_flag=slot.min_flag,
		max_flag=slot.max_flag, 
		color1=slot.colors['1'], 
		color2=slot.colors['-1'],
		sizeX=console.size.width,
		sizeY=slot.nr_studies*2+1,
		signal_as_line=False,
		dark_theme=True,
		brightness=True)
	console.print(signals)

	signal_as_line = True

	for study in slot.studies:

		series = study.config.indicator_1.raw
		if study.config.indicator_2 != None:
			series = [series]
			series.append(study.config.indicator_2.raw)

		s = Plot.line(
			series=series,
			signals=study.result,
			min_flag=0,
			max_flag=0,
			color1=slot.colors['1'], 
			color2=slot.colors['-1'],
			sizeX=console.size.width,
			sizeY=20,
			dark_theme=True,
			signal_as_line=signal_as_line,
			brightness=not signal_as_line)

		signal_as_line = not signal_as_line

		console.print(s)
		s_bar = Plot.study_bar(
			study=study,
			color1=slot.colors['1'],
			color2=slot.colors['-1'],
			sizeX=console.size.width,
			dark_theme=True,
			brightness=signal_as_line
			)
		console.print(s_bar)