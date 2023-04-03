__author__ = "pom11"
__copyright__ = "Copyright 2023, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "2.0.1"
__maintainer__ = "pom11"
__email__ = "office@parsecom.ro"

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Static
from rich.color import Color
from ..app import Slot
from ..plot import Plot
from .widgets import Graph, Footer, Time, Help


class Body(Container):
	pass

class TUI(App[None]):

	CSS = """
Screen {
	align: center middle;
	background: $surface;
	overflow: hidden;
	layers: base overlay notes notifications;
}

Graph {
	width: 100%;
	height: 100%;
}

Body {
	height: 100%;
	width: 100%;
}

Help {
	width: 80%;
	dock: right;
	layer: overlay;
}

Help:focus-within {
	offset: 0 0 !important;
}

Help.-hidden {
	offset-x: 100%;
}

Help Title {
    background: $surface;
    color: $secondary;
    padding: 2 4;
    border-right: vkey $background;
    dock: top;
    text-align: center;
    text-style: bold;
}

#line {
	width: 100%;
	height: auto;
	dock: top;
}

#signals {
	width: 100%;
	height: auto;
}

#time {
	width: 100%;
	height: auto;
}

#studies {
	width: 100%;
	height: auto;
}

#footer {
	width: 100%;
	height: auto;
	dock: bottom;
}
"""

	BINDINGS = [
		("r","refresh","Refresh"),
		("h","help","Help"),
		("q","quit","Quit"),
		("t", "theme", "Theme"),
		("s", "signal","Signal"),
		("b", "brightness","Brightness")
	]

	def __init__(self, **kwargs) -> None:
		if 'slot' in kwargs.keys():
			self.slot = kwargs['slot']
		else:
			self.slot = Slot(config='example')
		super().__init__()			

	def compose(self) -> ComposeResult:
		plots = []
		for layout in self.slot.layout:
			if layout in ['line','signals','studies']:
				widget = Graph(slot_init=self.slot, plot_type=layout)
			elif layout == 'time':
				widget = Time(slot=self.slot)
			elif layout == 'footer':
				widget = Footer(slot=self.slot)
			plots.append(
				Container(
					widget,
					id=layout
				)
			)
		yield Container(
			Help(classes="-hidden"),
			Body(
				*tuple(plots),
				id="contents"
				)
			)

	def on_mount(self) -> None:
		self.set_interval(1,self.refresh_graphs)
		self.compute_height()

	def on_resize(self) -> None:
		self.compute_height()

	def refresh_graphs(self) -> None:
		self.slot.ETA = self.slot.ETA-1
		if self.slot.ETA == 0:
			self.slot.refresh()
			# if self.slot.latest_signal == 0:
			# 	self.app.bell()
		
	def action_refresh(self) -> None:
		self.slot.refresh()

	def action_help(self) -> None:
		sidebar = self.query_one(Help)
		self.set_focus(None)
		if sidebar.has_class("-hidden"):
			sidebar.remove_class("-hidden")
		else:
			if sidebar.query("*:focus"):
				self.screen.set_focus(None)
			sidebar.add_class("-hidden")

	def action_brightness(self) -> None:
		for widget in [Graph,Time,Footer]:
			w = self.query(widget)
			if len(w)>0:
				for ww in w:
					ww.brightness = not ww.brightness

	def action_theme(self) -> None:
		self.dark = not self.dark
		for widget in [Graph,Time]:
			w = self.query(widget)
			if len(w)>0:
				for ww in w:
					ww.dark = self.dark

	def action_signal(self) -> None:
		graphs = self.query(Graph)
		for graph in graphs:
			graph.signal_as_line = not graph.signal_as_line
		
	def compute_height(self) -> None:
		_studies = self.slot.nr_studies if "studies" in self.slot.layout else 0
		_studies = 4 if self.slot.nr_studies <= 4 else _studies
		_signals = self.slot.nr_studies if "signals" in self.slot.layout else 0
		_signals = 4 if self.slot.nr_studies <= 4 else _signals
		_time = 1 if "time" in self.slot.layout else 0
		_footer = 1 if "footer" in self.slot.layout else 0

		height = {
			"line": self.size.height-_studies-_signals-_time-_footer,
			"studies": _studies,
			"signals": _signals,
			"time": _time,
			"footer": _footer
		}

		for layout in self.slot.layout:
			graphs = self.query(f"#{layout}")
			if len(graphs)>0:
				graphs.first().styles.height = height[layout]


if __name__ == "__main__":
	slot = Slot(config="example")
	app = TUI(slot=slot)
	app.run()

