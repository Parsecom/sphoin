from rich.text import Text
from rich.style import Style


uni_chars = {
	"space": u'\u0020',
	"vertical_bar":u'\u2524',
	"light":{
		"curved":{
			"horizontal": u'\u2500',
			"vertical": u'\u2502',
			"up_right": u'\u2570',
			"down_right": u'\u256D',
			"left_down": u'\u256E',
			"left_up": u'\u256F',
		},
		"angular":{
			"horizontal": u'\u2500',
			"vertical": u'\u2502',
			"up_right": u'\u2514',
			"down_right": u'\u250C',
			"left_down": u'\u2510',
			"left_up": u'\u2518'
		},
	},
	"heavy":{
		"angular":{
			"horizontal": u'\u2501',
			"vertical": u'\u2503',
			"up_right": u'\u2517',
			"down_right": u'\u250F',
			"left_down": u'\u2513',
			"left_up": u'\u251B'
		},
		"cross":{
			"full":{
				"light_horizontal": u'\u2542',
				"light_vertical": u'\u253F',
				"light_up_right": u'\u2545',
				"light_left_down": u'\u2544',
				"light_left_up": u'\u2546',
				"light_down_right": u'\u2543'
			},
			"vertical":{
				"light_right": u'\u2520',
				"light_left": u'\u2528',
				"left_down": u'\u252A',
				"left_up": u'\u2529',
				"up_right": u'\u2521',
				"down_right": u'\u2522'
			},
			"horizontal":{
				"light_up": u'\u2537',
				"light_down": u'\u252F',
				"left_down": u'\u2531',
				"left_up": u'\u2539',
				"up_right": u'\u253A',
				"down_right": u'\u2532'
			}
		}
	}
}

footer = {
	"display": {
		"left":{
			"s": "{market}{interval}|{max_flag}|{min_flag}|",			
			"m": "{market} | {interval}| {max_flag}| {min_flag}|",
			"l": "{exchange}|{market}|{interval}|{max_flag}|{min_flag}|",
			"xl":" {exchange} | {market} | {interval} | {max_flag} | {min_flag} |"
			},
		"mid":{
			"s": "|h|q|r|t|s",
			"m": "| h | q | r | t | s ",
			"l": "|h Help|q Quit|r Refresh|t Theme|s Signal",
			"xl":"| h Help | q Quit | r Refresh | t Theme | s Signal ",
			},
		"right":{
			"s": "|{eta}",
			"m": "| {eta} ",
			"l": "|ETA {eta}",
			"xl":"| ETA {eta} "
			}
	},
	"color":{
		"exchange":{
			"color":"black",
			"bgcolor":"yellow"
		},
		"market":{
			"color":"black",
			"bgcolor":"white"
		},
		"interval":{
			"color":"black",
			"bgcolor":"white"
		},
		"max_flag":{
			"color":"black",
			"bgcolor":"yellow"
		},
		"min_flag":{
			"color":"black",
			"bgcolor":"yellow"
		},
	},
	"actions": {
		"help":[" h Help ","h Help"," h ","h"],
		"quit":[" q Quit ","q Quit"," q ","q"],
		"refresh":[" r Refresh ","r Refresh"," r ","r"],
		"theme":[" t Theme ","t Theme"," t ","t"],
		"signal":[" s Signal ","s Signal"," s ","s"]
	}
}

def intersperse(_list: list, item):
	result = [item] * (len(_list) * 2 -1)
	result[0::2] = _list
	return result

def text_with_style(
	string: str,
	fg: str,
	bg: str) -> tuple:
	return [string,f"{fg} on {bg}"]

def isNumber(n) -> bool:
	return not n == None