__author__ = "pom11"
__copyright__ = "Copyright 2023, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "2.0.10"
__maintainer__ = "pom11"
__email__ = "office@parsecom.ro"

import typing
from importlib import import_module

if typing.TYPE_CHECKING:
	from ._footer import Footer
	from ._graph import Graph
	from ._time import Time
	from ._help import Help

__all__ = [
	"Footer",
	"Graph",
	"Time",
	"Help"
]

__cache = {}

def __getattr__(string):
	try:
		return __cache[string]
	except KeyError:
		pass

	if string not in __all__:
		raise ImportError(f"Package 'sphoin.tui.widgets' has no class '{string}'")

	module = import_module(f"._{string.lower()}", package="sphoin.tui.widgets")
	class__ = getattr(module, string)

	__cache[string] = class__
	return class__