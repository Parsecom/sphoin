from textual.reactive import reactive
from textual.widgets import Static
from rich.text import Text, Span
from rich.style import Style
from rich.color import Color
from ...app import Slot
from ...plot import Plot
from ...utils import footer, text_with_style, uni_chars
import datetime

class Footer(Static):

	slot : [Slot, None] = reactive(None)
	banner : list = reactive([Text("Painting..")])
	brightness : bool = reactive(False)

	def __init__(self, slot: Slot) -> None:
		self._slot = slot
		super().__init__()

	def paint_banner(self, slot: Slot, brightness: bool) -> list:
		if self.size.width <50:
			return [Text()]
		if slot!=None:
			bright = "bright_" if brightness else ""
			eta = datetime.timedelta(seconds=int(slot.ETA))
			formatted = {
			"exchange":slot.exchange,
			"market":slot.market,
			"interval":slot.interval,
			"max_flag":slot.max_flag,
			"min_flag":slot.min_flag
			}
			color = footer['color']
			color['max_flag']['bgcolor'] = slot.colors['1']
			color['min_flag']['bgcolor'] = slot.colors['-1']
			sizes = {
				"left":{
					"s":Text(footer["display"]["left"]["s"].format(**formatted)),
					"m":Text(footer["display"]["left"]["m"].format(**formatted)),
					"l":Text(footer["display"]["left"]["l"].format(**formatted)),
					"xl":Text(footer["display"]["left"]["xl"].format(**formatted))
				},
				"mid":{
					"s":Text(footer["display"]["mid"]["s"]),
					"m":Text(footer["display"]["mid"]["m"]),
					"l":Text(footer["display"]["mid"]["l"]),
					"xl":Text(footer["display"]["mid"]["xl"]),
				},
				"right":{
					"s":Text(footer["display"]["right"]["s"].format(eta=eta)),
					"m":Text(footer["display"]["right"]["m"].format(eta=eta)),
					"l":Text(footer["display"]["right"]["l"].format(eta=eta)),
					"xl":Text(footer["display"]["right"]["xl"].format(eta=eta))
				}
			}
			size = ["xl","l","m","s"]
			for r in size:
				tright = sizes["right"][r]
				tright.stylize(Style(color="black",bgcolor=f"{bright}white"))
				right = len(tright)
				for l in size:
					tleft = sizes["left"][l]
					spans = []
					for key, value in formatted.items():
						_values = [f" {value} |",f"{value} |",f"{value}|",f"{value}"]
						for value in _values:
							exists = value in str(tleft)
							if exists:
								start = str(tleft).index(str(value))
								end = str(tleft).index(str(value))+len(str(value))
								spans.append(Span(start=start,end=end,style=Style(color=color[key]['color'],bgcolor=f"{bright}{color[key]['bgcolor']}")))
								break
					tleft.spans = spans
					left = len(tleft)				
					for m in size:
						tmid = sizes["mid"][m]
						for action in footer['actions'].keys():
							for key in footer["actions"][action]:
								if key in tmid:
									tmid.stylize(Style(color="black",bgcolor=f"{bright}yellow"))
									tmid.stylize(Style.on(click=action),start=str(tmid).index(key),end=str(tmid).index(key)+len(key))
									break
						mid = len(tmid)
						spare = self.size.width - right - left - mid
						if spare >= 0:
							return [tleft,Text.from_ansi(uni_chars["space"]*spare),tmid,tright]
		else:
			return [Text()]

	def on_mount(self) -> None:
		self.slot = self._slot
		self.styles.link_background = "yellow"
		self.styles.link_style = "bold"
		self.styles.link_hover_style = "bold italic"
		self.styles.link_hover_background = "magenta"

		self.set_interval(1, self.refresh_banner)

	def refresh_banner(self) -> None:
		self.banner = self.paint_banner(slot=self.slot,brightness=self.brightness)

	def watch_banner(self, banner: list) -> None:
		string = Text()
		for text in banner:
			string += text
		self.update(string)

	def watch_slot(self, slot: Slot) -> None:
		self.banner = self.paint_banner(slot=slot, brightness=self.brightness)

	def watch_brightness(self, brightness: bool) -> None:
		self.banner = self.paint_banner(slot=self.slot, brightness=brightness)


