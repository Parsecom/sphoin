from textual.reactive import reactive
from textual.widgets import Static
from rich.text import Text
from ...app import Slot
from ...plot import Plot

class Time(Static):

	slot : [Slot, None] = reactive(None)
	brightness: bool = reactive(False)
	banner : Text = reactive(Text(""))
	dark: bool = reactive(True)

	def __init__(self, slot: Slot) -> None:
		self._slot = slot
		super().__init__()

	def paint_time(self, slot: Slot, dark: bool, brightness: bool) -> Text:
		if self.size.width<50:
			return ''
		return Plot.time_bar(slot=slot,sizeX=self.size.width,dark_theme=dark,brightness=brightness)

	def on_mount(self) -> None:
		self.slot = self._slot
		self.set_interval(1, self.refresh_banner)

	def refresh_banner(self) -> None:
		self.banner = self.paint_time(slot=self.slot, dark=self.dark, brightness=self.brightness)

	def watch_brightness(self, brightness: bool) -> None:
		self.banner = self.paint_time(slot=self.slot,dark=self.dark,brightness=brightness)

	def watch_banner(self, banner: Text) -> None:
		self.update(banner)

	def watch_slot(self, slot: Slot) -> None:
		if slot!=None:
			self.banner = self.paint_time(slot=slot,dark=self.dark,brightness=self.brightness)

	def watch_dark(self, dark: bool) -> None:
		self.banner = self.paint_time(slot=self.slot,dark=dark,brightness=self.brightness)