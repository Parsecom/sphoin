

import datetime
from dateutil import tz
from ..models import Ohlcv, Study
from ..app import Slot
from ..utils import isNumber, uni_chars, intersperse, text_with_style
from rich.color import Color, ANSI_COLOR_NAMES
from rich.text import Text
from rich.style import Style
from math import floor, ceil

class Plot:
	"""
Plot module for sphoin.app Slots

Methods
-------
line
    Generate an ascii chart for a series of numbers
study_bar
    Generate an ascii bar chart for a series of numbers
time_bar
    Generate an ascii time bar for a series of numbers
	"""

	def __init__(self):
		pass

	def line(
		series: list,
		signals: list,
		min_flag: int = 0,
		max_flag: int = 0,
		color1: str = 'magenta', 
		color2: str = 'cyan',
		sizeY: int = 200, 
		sizeX: int = 50,
		signal_as_line: bool = False,
		dark_theme: bool = True,
		brightness: bool = True) -> str:

		"""
Generate an ascii chart for a series

Parameters
----------
series : list
    List of values to chart
signals : list
    List of signals corresponding to each series element
min_flag : int
    Filter signals lower or equal with min_flag
max_flag : int
	Filter signals bigger or equal with max_flag
color1 : str
	rich ansi color name
	Default : magenta
	see 'python -m rich.color'
color2 : str
	rich ansi color name
	Default : cyan
	see 'python -m rich.color'
sizeY : int
	Height of chart plot
	Default : 200
	Constraints
		min : 4
		max : 200
sizeX : int
	Width of chart plot
	Default : 50
	Contraints
		min : 50
		max : 500
signal_as_line : bool
	Plots signal as vertical line (True) or dot (False)
	Default : False
dark_theme : bool
	Theme of chart plot
	Default : True
brightness : bool
	Default : True

Returns
------
rich Text
	Ansi chart
		"""

		if len(series) == 0:
			return Text()
		if len(signals) == 0:
			return Text()

		
		if sizeY < 4:
			sizeY = 4
		elif sizeY > 200:
			sizeY = 200
		if sizeX < 50:
			sizeX = 50
			# crop = -sizeX+11
		elif sizeX > 500:
			sizeX = 500
		crop = -sizeX+11

		sizeY -= 1

		bright = "bright_" if brightness else ""
		line_type = "curved"
		line_color = f"{bright}white" if dark_theme else "black"
		background_color = "black" if dark_theme else f"{bright}white"
		color1 = f"{bright}{color1}"
		color2 = f"{bright}{color2}"

		offset = 1
		if not isinstance(series[0],list):
			if all(not isNumber(n) for n in series):
				return Text()
			else:
				if len(series)+12<=sizeX:
					sizeX = len(series)+12
					crop = 0
				series = [series[crop:]]

		else:
			if len(series[0])+12<=sizeX:
				sizeX = len(series[0])+12
				crop = 0
			line_type = "angular"
			series = [x[crop:] for x in series]

		signals = signals[crop:]
		minimum = min(filter(isNumber, [y for x in series for y in x]))
		maximum = max(filter(isNumber, [y for x in series for y in x]))
		interval = abs(float(maximum) - float(minimum))
		interval = 0.1 if interval == 0 else interval
		ratio = (sizeY) / interval
		intmin2 = int(round(float(minimum) * ratio))
		intmax2 = int(round(float(maximum) * ratio))

		rows = abs(intmax2 - intmin2)

		width = 0
		for i in range(0,len(series)):
			width = max(width, len(series[i]))
		width += offset

		result = [[text_with_style(string=uni_chars["space"],fg=line_color,bg=background_color)] * (width-offset) for i in range(rows+1)]

		for y in range(intmin2, intmax2 + 1):
			try:
				label = '{:8.9f}'.format(float(maximum) - ((y - intmin2) * interval / rows))[:11]
			except Exception as e:
				label = '{:8.9f}'.format(0)
			result[y - intmin2][max(offset - len(label), 0)] = text_with_style(string=label+uni_chars["vertical_bar"],fg=line_color,bg=background_color)

		font_weights =["light","heavy"]
		for i in range(0, len(series)):
			font_weight = font_weights[i]
			for x in range(0, len(series[i])-1):
				try:
					y0 = int(round(series[i][x + 0] * ratio) - intmin2)
					y1 = int(round(series[i][x + 1] * ratio) - intmin2)
				except Exception as e:
					y0 = 0
					y1 = 0
				if y0 == y1:
					horizontal = uni_chars[font_weight][line_type]["horizontal"]
					if i == 1:
						if uni_chars["light"][line_type]["up_right"] in result[rows - y0][x + offset]:
							horizontal = uni_chars["heavy"]["cross"]["horizontal"]["light_up"]
						elif uni_chars["light"][line_type]["left_up"] in result[rows - y0][x + offset]:
							horizontal = uni_chars["heavy"]["cross"]["horizontal"]["light_up"]
						elif uni_chars["light"][line_type]["vertical"] in result[rows - y0][x + offset]:
							horizontal = uni_chars["heavy"]["cross"]["full"]["light_vertical"]
						elif uni_chars["light"][line_type]["down_right"] in result[rows - y0][x + offset]:
							horizontal = uni_chars["heavy"]["cross"]["horizontal"]["light_down"]
						elif uni_chars["light"][line_type]["left_down"] in result[rows - y0][x + offset]:
							horizontal = uni_chars["heavy"]["cross"]["horizontal"]["light_down"]
					paint0 = text_with_style(string=horizontal,fg=line_color,bg=background_color)
					try:#background from signal
						if signals[x]>=max_flag:
							paint0 = text_with_style(string=horizontal,fg="black",bg=color1)
						elif signals[x]<=min_flag:
							paint0 = text_with_style(string=horizontal,fg="black",bg=color2)
					except:
						pass
					result[rows - y0][x + offset] = paint0
				else:
					if y0 > y1:
						going_lower1 = uni_chars[font_weight][line_type]["up_right"]
						if i == 1:
							if uni_chars["light"][line_type]["horizontal"] in result[rows - y1][x + offset]:
								going_lower1 = uni_chars["heavy"]["cross"]["horizontal"]["up_right"]
							elif uni_chars["light"][line_type]["left_up"] in result[rows - y1][x + offset]:
								going_lower1 = uni_chars["heavy"]["cross"]["horizontal"]["up_right"]
							elif uni_chars["light"][line_type]["vertical"] in result[rows - y1][x + offset]:
								going_lower1 = uni_chars["heavy"]["cross"]["vertical"]["up_right"]
							elif uni_chars["light"][line_type]["down_right"] in result[rows - y1][x + offset]:
								going_lower1 = uni_chars["heavy"]["cross"]["vertical"]["up_right"]
							elif uni_chars["light"][line_type]["left_down"] in result[rows - y1][x + offset]:
								going_lower1 = uni_chars["heavy"]["cross"]["full"]["light_left_down"]
						paint1 = text_with_style(string=going_lower1,fg=line_color,bg=background_color)
						try:
							if signals[x]>=max_flag:
								paint1 = text_with_style(string=going_lower1,fg="black",bg=color1)
							elif signals[x]<=min_flag:
								paint1 = text_with_style(string=going_lower1,fg="black",bg=color2)
						except:
							pass
						result[rows - y1][x + offset] = paint1
						
						going_lower2 = uni_chars[font_weight][line_type]["left_down"]
						if i == 1:
							if uni_chars["light"][line_type]["horizontal"] in result[rows - y0][x + offset]:
								going_lower2 = uni_chars["heavy"]["cross"]["horizontal"]["left_down"]
							elif uni_chars["light"][line_type]["left_up"] in result[rows - y0][x + offset]:
								going_lower2 = uni_chars["heavy"]["cross"]["vertical"]["left_down"]
							elif uni_chars["light"][line_type]["vertical"] in result[rows - y0][x + offset]:
								going_lower2 = uni_chars["heavy"]["cross"]["vertical"]["left_down"]
							elif uni_chars["light"][line_type]["down_right"] in result[rows - y0][x + offset]:
								going_lower2 = uni_chars["heavy"]["cross"]["horizontal"]["left_down"]
							elif uni_chars["light"][line_type]["up_right"] in result[rows - y0][x + offset]:
								going_lower2 = uni_chars["heavy"]["cross"]["full"]["light_up_right"]
						paint2 = text_with_style(string=going_lower2,fg=line_color,bg=background_color)
						try:
							if signals[x]>=max_flag:
								paint2 = text_with_style(string=going_lower2,fg="black",bg=color1)
							elif signals[x]<=min_flag:
								paint2 = text_with_style(string=going_lower2,fg="black",bg=color2)
						except:
							pass
						result[rows - y0][x + offset] = paint2
					
					elif y0 < y1:
						going_up1 = uni_chars[font_weight][line_type]["down_right"]
						if i == 1:
							if uni_chars["light"][line_type]["horizontal"] in result[rows - y1][x + offset]:
								going_up1 = uni_chars["heavy"]["cross"]["horizontal"]["down_right"]
							elif uni_chars["light"][line_type]["left_up"] in result[rows - y1][x + offset]:
								going_up1 = uni_chars["heavy"]["cross"]["full"]["light_left_up"]
							elif uni_chars["light"][line_type]["vertical"] in result[rows - y1][x + offset]:
								going_up1 = uni_chars["heavy"]["cross"]["vertical"]["down_right"]
							elif uni_chars["light"][line_type]["up_right"] in result[rows - y1][x + offset]:
								going_up1 = uni_chars["heavy"]["cross"]["vertical"]["down_right"]
							elif uni_chars["light"][line_type]["left_down"] in result[rows - y1][x + offset]:
								going_up1 = uni_chars["heavy"]["cross"]["horizontal"]["down_right"]
						paint1 = text_with_style(string=going_up1,fg=line_color,bg=background_color)
						try:
							if signals[x]>=max_flag:
								paint1 = text_with_style(string=going_up1,fg="black",bg=color1)
							elif signals[x]<=min_flag:
								paint1 = text_with_style(string=going_up1,fg="black",bg=color2)
						except:
							pass
						result[rows - y1][x + offset] = paint1
						
						going_up2 = uni_chars[font_weight][line_type]["left_up"]
						if i == 1:
							if uni_chars["light"][line_type]["horizontal"] in result[rows - y0][x + offset]:
								going_up2 = uni_chars["heavy"]["cross"]["horizontal"]["left_up"]
							elif uni_chars["light"][line_type]["down_right"] in result[rows - y0][x + offset]:
								going_up2 = uni_chars["heavy"]["cross"]["full"]["light_down_right"]
							elif uni_chars["light"][line_type]["vertical"] in result[rows - y0][x + offset]:
								going_up2 = uni_chars["heavy"]["cross"]["vertical"]["left_up"]
							elif uni_chars["light"][line_type]["up_right"] in result[rows - y0][x + offset]:
								going_up2 = uni_chars["heavy"]["cross"]["horizontal"]["left_up"]
							elif uni_chars["light"][line_type]["left_down"] in result[rows - y0][x + offset]:
								going_up2 = uni_chars["heavy"]["cross"]["vertical"]["left_up"]
						paint2 = text_with_style(string=going_up2,fg=line_color,bg=background_color)
						try:
							if signals[x]>=max_flag:
								paint2 = text_with_style(string=going_up2,fg="black",bg=color1)
							elif signals[x]<=min_flag:
								paint2 = text_with_style(string=going_up2,fg="black",bg=color2)
						except:
							pass
						result[rows - y0][x + offset] = paint2

					start = min(y0, y1) + 1
					end = max(y0, y1)
					for y in range(start, end):
						vertical = uni_chars[font_weight][line_type]["vertical"]
						if i == 1:
							if uni_chars["light"][line_type]["up_right"] in result[rows - y][x + offset]:
								vertical = uni_chars["heavy"]["cross"]["vertical"]["light_right"]
							elif uni_chars["light"][line_type]["left_up"] in result[rows - y][x + offset]:
								vertical = uni_chars["heavy"]["cross"]["vertical"]["light_left"]
							elif uni_chars["light"][line_type]["horizontal"] in result[rows - y][x + offset]:
								vertical = uni_chars["heavy"]["cross"]["full"]["light_horizontal"]
							elif uni_chars["light"][line_type]["down_right"] in result[rows - y][x + offset]:
								vertical = uni_chars["heavy"]["cross"]["vertical"]["light_right"]
							elif uni_chars["light"][line_type]["left_down"] in result[rows - y][x + offset]:
								vertical = uni_chars["heavy"]["cross"]["vertical"]["light_left"]
						paint3 = text_with_style(string=vertical,fg=line_color,bg=background_color)
						try:
							if signals[x]>=max_flag:
								paint3 = text_with_style(string=vertical,fg="black",bg=color1)
							elif signals[x]<=min_flag:
								paint3 = text_with_style(string=vertical,fg="black",bg=color2)
						except:
							pass
						result[rows - y][x + offset] = paint3

		if signal_as_line:
			for j in range(len(result[0])):
				col = [row[j] for row in result]
				if any(color1 in x[1] for x in col):
					for i in range(len(result)):
						if background_color in result[i][j][1]:
							result[i][j] = text_with_style(string=result[i][j][0],fg="black",bg=color1)
				elif any(color2 in x[1] for x in col):
					for i in range(len(result)):
						if background_color in result[i][j][1]:
							result[i][j] = text_with_style(string=result[i][j][0],fg="black",bg=color2)

		ret = []
		for row in result:
			r = []
			for item in row:
				r.append(tuple(item))
			ret.append(Text.assemble(*tuple(r),end=""))
		ret = intersperse(ret,Text("\n"))
		ret = Text.assemble(*tuple(ret))
		return ret

	def study_bar(
		study: Study,
		color1: str = 'magenta', 
		color2: str = 'cyan', 
		sizeX: int = 50,
		dark_theme: bool = True,
		brightness: bool = True) -> Text:
		"""
Generate an ascii bar chart for Sphoin Slot Study

Parameters
----------
study : Study
    Sphoin Slot Study
    Example:
    	slot = Slot(config='example')
    	study = slot.studies[0]
color1 : str
	rich ansi color name
	Default : 'magenta'
	see 'python -m rich.color'
color2 : str
	rich ansi color name
	Default : 'cyan'
	see 'python -m rich.color'
sizeX : int
	Width of chart plot
	Default : 50
	Contraints
		min : 50
		max : 500
dark_theme : bool
	Theme of chart plot
	Default : True
brightness : bool
	Default : True

Returns
------
rich Text
	Ansi chart
		"""
		bright = "bright_" if brightness else ""
		if sizeX < 50:
			sizeX = 50
		elif sizeX > 500:
			sizeX = 500
		crop = -sizeX+11
		if len(study.result)+12<=sizeX:
			sizeX = len(study.result)+12
			crop = 0
		line_color = f"{bright}white" if dark_theme else "black"
		background_color = "black" if dark_theme else f"{bright}white"
		vv = 8 if bright else 0
		bgstudy = [k for k,v in ANSI_COLOR_NAMES.items() if v-vv==int(study.code.split("#")[1])][0]
		inter = study.study.center(11,uni_chars["space"]) + uni_chars["light"]["angular"]["vertical"]
		inter = [Text.assemble(tuple(text_with_style(string=inter,fg='black',bg=bgstudy)))]
		series = study.result[crop:]
		for i in range(0,len(series)-1):
			if series[i] == None or int(series[i])==0:
				inter.append(text_with_style(string=uni_chars['space'],fg=line_color,bg=background_color))
			elif int(series[i]) == 1:
				inter.append(text_with_style(string=uni_chars['space'],fg=line_color,bg=f"{bright}{color1}"))
			elif int(series[i]) == -1:
				inter.append(text_with_style(string=uni_chars['space'],fg=line_color,bg=f"{bright}{color2}"))
		
		return Text.assemble(*tuple(inter))

	def time_bar(
		slot: Slot, 
		sizeX: int = 50,
		dark_theme: bool = True,
		brightness: bool = True) -> str:
		"""
Generate an ascii time bar for a Sphoin Slot

Parameters
----------
slot : Slot
    Sphoin Slot 
    Example :
    	slot = Slot(config='example')
sizeX : int
	Width of chart plot
	Default : 50
	Contraints
		min : 50
		max : 500
dark_theme : bool
	Theme of chart plot
	Default : True
brightness : bool
	Default : True
Returns
------
rich Text
	Ansi chart
		"""
		if sizeX < 50:
			sizeX = 50
		elif sizeX > 500:
			sizeX = 500
		crop = -sizeX+11
		if len(slot.ohlcv.date)+12<=sizeX:
			sizeX = len(slot.ohlcv.date)+12
			crop = 0
		from_zone = tz.tzutc()
		to_zone = tz.tzlocal()
		bright = "bright_" if brightness else ""
		line_color = f"{bright}white" if dark_theme else "black"
		background_color = "black" if dark_theme else f"{bright}white"
		series = slot.ohlcv.date[crop:]
		result = []	
		visible_length = divmod(len(series),6)
		indices = [6*x+2 for x in range(visible_length[0])]
		for index in indices:
			try:
				current_date = datetime.datetime.strptime(series[-index-1], "%Y-%m-%dT%H:%M:%S")
			except Exception as e:
				current_date = datetime.datetime.strptime(series[-index-1].split(".")[0], "%Y-%m-%d %H:%M:%S")
			current_date = current_date.replace(tzinfo=from_zone)
			current_date = current_date.astimezone(to_zone)
			if slot.interval[-1] in ["m","h"]:
				current_date = current_date.strftime("%H:%M")
			else:
				current_date = current_date.strftime("%d/%m")
			date = text_with_style(string=current_date.rjust(6,' '),fg=line_color,bg=background_color)
			result.insert(0,date)
		_times = Text.assemble(*tuple(result))
		_label = Text.assemble(tuple(text_with_style(string='time'.rjust(12,'·'),fg="black",bg=f"{bright}yellow")))
		_add = sizeX - len(_times) - len(_label)
		if _add<0:
			result[0][0] = result[0][0][abs(_add):]
			_times = Text.assemble(*tuple(result))
		elif 0<_add<6:
			if crop==0:
				_add -= 1
			result.insert(0,text_with_style(string=uni_chars['space']*_add,fg=line_color,bg=background_color))
			_times = Text.assemble(*tuple(result))
		return Text.assemble(_label,_times)

