from textual.widgets import MarkdownViewer, Static
from textual.containers import Container
from textual.app import ComposeResult
from textual.reactive import reactive
from rich.text import Text

md = """\
# TUI key bindings

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

## Docker
```
docker pull pom11/sphoin
```

## `.yaml` config file
```yaml
---
uid: 111YOURUID111
api-key: 111YOURAPIKEY111
api-secret: 111YOURSECRET111
layout:
  - line
  - time
  - signals
  - studies
  - footer
  
```

In `layout` specifies what `Plot`s should be displayed

* `line` - Price graph
* `time` - Time bar
* `signals` - Signals sum graph
* `studies` - Studies bars
* `footer` - Footer with Slot details

# Usage

## CLI
```
sphoin --help
```
View example
```
sphoin --example
```
Load config file
```
sphoin --config config.yaml
```
Print Plot test
```
sphoin --plot
sphoin.plot
```

## Docker
Pull image from docker hub
```shell
docker pull pom11/sphoin
```
To run sphoin TUI with `config` file in docker you need to mount local directory to `/usr/src/app`
```shell
docker run -v ${PWD}/config.yaml:/usr/src/app/config.yaml -it pom11/sphoin -c config.yaml
``` 


## Python

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
