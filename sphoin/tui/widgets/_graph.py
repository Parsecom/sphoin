from textual.reactive import reactive
from textual.widgets import Static
from rich.text import Text
from rich.style import Style
from ...app import Slot
from ...plot import Plot
from ...utils import intersperse


class Graph(Static):

	plot : Text = reactive(Text(""))
	slot : [Slot, None] = reactive(None)
	plot_type : [str, None] = reactive(None)
	dark : bool = reactive(True)
	brightness : bool = reactive(False)
	signal_as_line : bool = reactive(True)

	def __init__(self, slot_init: Slot, plot_type: str) -> None:
		self._slot = slot_init
		self._plot_type = plot_type
		super().__init__()


	def paint_plot(self, slot: Slot, plot_type: str, dark: bool, brightness: bool) -> str:
		if self.size.width<50:
			return f"Screen width too small: {self.size.width}\nMin: 50"
		elif self.size.width>500:
			return f"Screen width too big: {self.size.width}\nMax: 500"
		if self.size.height<4:
			return f"Screen height too small: {self.size.height}\nMin: 4"
		elif self.size.height>200:
			return f"Screen height too big: {self.size.height}\nMax: 200"
		if slot != None:
			try:
				if plot_type == 'line':
					new_plot = Plot.line(
						series=slot.ohlcv.close,
						signals=slot.signals_sum,
						min_flag=slot.min_flag,
						max_flag=slot.max_flag, 
						color1=self.slot.colors['1'], 
						color2=self.slot.colors['-1'],
						sizeX=self.size.width,
						sizeY=self.size.height,
						signal_as_line=self.signal_as_line,
						dark_theme=dark,
						brightness=brightness)
					return new_plot
				elif plot_type == 'studies':
					new_plot = []
					for study in slot.studies:
						new_plot.append(Plot.study_bar(
						study=study,
						color1=slot.colors['1'],
						color2=slot.colors['-1'],
						sizeX=self.size.width,
						dark_theme=dark,
						brightness=brightness
						))
					new_plot = intersperse(new_plot,Text("\n"))
					return Text.assemble(*tuple(new_plot))
				elif plot_type == 'signals':
					new_plot = Plot.line(
						series=slot.signals_sum,
						signals=slot.signals_sum,
						min_flag=slot.min_flag,
						max_flag=slot.max_flag, 
						color1=slot.colors['1'], 
						color2=slot.colors['-1'],
						sizeX=self.size.width,
						sizeY=self.size.height,
						signal_as_line=self.signal_as_line,
						dark_theme=dark,
						brightness=brightness)
					return new_plot
			except Exception as e:
				return Text(f"{e}")
		else:
			return Text("Painting...")


	def on_mount(self) -> None:
		self.slot = self._slot
		self.plot_type = self._plot_type
		self.set_interval(1,self.refresh_plot)

	def refresh_plot(self) -> None:
		self.plot = self.paint_plot(slot=self.slot,plot_type=self.plot_type,dark=self.dark, brightness=self.brightness)

	def watch_plot(self, plot: Text) -> None:
		self.update(plot)

	def watch_brightness(self, brightness: bool) -> None:
		self.brightness = brightness
		self.plot = self.paint_plot(slot=self.slot,plot_type=self.plot_type, dark=self.dark, brightness=brightness)

	def watch_dark(self, dark: bool) -> None:
		self.dark = dark
		self.plot = self.paint_plot(slot=self.slot,plot_type=self.plot_type, dark=dark, brightness=self.brightness)

	def watch_slot(self, slot: str) -> None:
		self.plot = self.paint_plot(slot=slot,plot_type=self.plot_type, dark=self.dark, brightness=self.brightness)

	def watch_plot_type(self, plot_type: str) -> None:
		self.plot = self.paint_plot(slot=self.slot,plot_type=plot_type, dark=self.dark, brightness=self.brightness)
