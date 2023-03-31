from textual.widgets import MarkdownViewer, Static
from textual.containers import Container
from textual.app import ComposeResult
from textual.reactive import reactive
from rich.text import Text

md = """\

# TUI

## Key bindings

* h - Help sidebar
* r - Refresh Slot data
* t - Toggle theme
* s - Signals theme
* b - Toggle brightness
* q - Quit

# Installation

## Stable release
To install sphoin, run this command in your terminal:

```
pip install sphoin
```

This is the preferred method to install sphoin, as it will always install the most recent stable release.

## From sources

The sources for sphoin can be downloaded from the `Github repo`.
* clone the public repository
```
git clone https://github.com/Parsecom/sphoin
```
* install from source
```
python setup.py install
```
# Usage
## config.yaml configuration file template
```yaml
-----
uid: 111YOURUID111
api-key: 111YOURAPIKEY111
api-secret: 111YOURSECRET111
layout:
  - line
  - time
  - signals
  - studies
  - banner
```

## TUI:
```
sphoin --help
```
View example
```
sphoin --example
```
Load config file
```
sphoin --file config.yaml
```

## To use sphoin in a python project:

Import package:
```python
from sphoin.app import Slot
from rich import print
from rich import inspect
```
Init Slot with token and secret:
```python
my_slot = Slot(uid="111YOURUID111",
			api_key="111YOURAPIKEY111",
			api_secret="111YOURSECRET111")
print(my_slot.json)
# insepct slot attributes
print(my_slot.__doc__)
print(inspect(my_slot,all=True))
```

"""

class Title(Static):
	pass


class Help(Container):

	def compose(self) -> ComposeResult:
		yield Title(Text.from_markup("[bold cyan]sphoin[/][bold magenta].app[/] [bold yellow]TUI[/]"))
		yield MarkdownViewer(md, show_table_of_contents=True)
