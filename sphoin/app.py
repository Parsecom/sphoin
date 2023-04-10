"""Main module."""

__author__ = "pom11"
__copyright__ = "Copyright 2023, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "2.0.10"
__maintainer__ = "pom11"
__email__ = "office@parsecom.ro"

import requests
import json
import yaml
import time
import sys,select
import os
import datetime as dt
from sphoin.models import Ohlcv, Study

class Slot:
	"""
Slot class to represent a sphoin.app Slot

Example config.yaml input file
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


Attributes
----------
status : str
	Slot status
error : str
	Slot error
api_key : str
	Api Key
api_secret : str
	Api Secret
uid : str
	User id
exchange : str
	Exchange
market : str
	Market
interval : str
	Interval
min_flag : int
	Filter signals lower or equal with min_flag
max_flag : int
	Filter signals bigger or equal with max_flag
ETA : int
	Seconds till next update
latest_signal : int
	Latest signal
signals_sum : list
	List of ints with sum of all signals
colors : dict
	Dict with rich color names corresponding to -1 and 1 signals
nr_studies : int
	Number of configured Sphoin Studies
studies : list
	List of configured sphoin Studies

layout : list
	TUI layout config
	Expected values: line, studies, signals

Methods
------
refresh
	Manually fetches Slot result

Returns
-------
Slot
	"""
	def __init__(self) -> None:
		self.show_banner : bool = False
		self.base_url : str = "https://api.sphoin.app/api/v1"

	def refresh(self):
		"""
Updates Slot attributes with new values
		"""
		self.__get_json()

	def __get_screenSize(self, data: dict = {}):
		"""
Get console size from dict

Parameters
----------
data : dict
		"""
		if "sizeX" in data.keys():
			self.sizeX : int = data['sizeX']
		else:
			self.sizeX : int = None
		if "sizeY" in data.keys():
			self.sizeY : int = data['sizeY']
		else:
			self.sizeY : int = None

	@classmethod
	def from_config(cls, file: str = 'example') -> "Slot":
		"""
Init Slot from config file

Example config.yaml input file
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
Example
	my_slot = Slot.from_config(file='/aboslute/path/of/config.yaml')

Parameters
----------
file : str
	Absolute path of yaml config file
	Default : example
		Inits Slot with example configuration

Returns
-------
Slot
		"""
		if not file:
			raise ValueError("config")
		slot = cls()
		slot.config = file
		if file != "example":
			with open(file,"r") as f:
				data = yaml.safe_load(f)
		else:
			data = {
				"uid" : "111YOURUID111",
				"api-secret" : "111YOURSECRET111",
				"api-key":"111YOURAPIKEY111",
				"layout" : [
					"line",
					"time",
					"studies",
					"signals",
					"footer"
					]
				}
		slot.api_key : str = data["api-key"]
		slot.api_secret : str = data["api-secret"]
		slot.uid : str = data["uid"]
			
		try:
			if not isinstance(data["layout"],list):
				raise ValueError("layout not list")
			elif not any([x in data["layout"] for x in ['line','studies','signals','time','footer']]):
				raise ValueError("layout expected values: line, studies, signals, time, footer")
			else:
				slot.layout : list = data["layout"]
		except Exception as e:
			slot.layout = [
					"line",
					"time",
					"studies",
					"signals",
					"footer"
					]

		slot.__get_screenSize(data)
		slot.__get_json()
		return slot
		
	@classmethod
	def from_keys(cls, api_key: str = None, api_secret: str = None, uid: str = None, layout: list = None, sizeX: int = None, sizeY: int = None) -> "Slot":
		"""
Init Slot from keys

Example:
	my_slot = Slot.from_keys(api_key='111YOURAPIKEY111',api_secret='111YOURSECRET111',uid='111YOURUID111')

Parameters
----------
api_key : str
	Api Key
secret_key : str
	Secret Key
uid : str
	User id
layout : list
	TUI layout
sizeX : int
	Width of console
sizeY : int
	Height of console

Returns
-------
Slot
		"""
		slot = cls()
		slot.config = None
		if not api_key:
			raise ValueError("api_key")
		if not api_secret:
			raise ValueError("api_secret")
		if not uid:
			raise ValueError("uid")
		slot.api_key : str = api_key
		slot.api_secret : str = api_secret
		slot.uid : str = uid
		try:
			if layout:
				if not isinstance(kwargs["layout"],list):
					raise ValueError("layout not list")
				elif not any([x in kwargs["layout"] for x in ['line','studies','signals','time','footer']]):
					raise ValueError("layout list expected values: line, studies, signals, time, footer")
				else:
					slot.layout : list = kwargs["layout"]
			else:
				raise ValueError("layout list missing")
		except Exception as e:
			slot.layout = [
					"line",
					"time",
					"studies",
					"signals",
					"footer"
					]

		slot.__get_screenSize({"sizeX":sizeX,"sizeY":sizeY})
		slot.__get_json()
		return slot

	@classmethod
	def from_dict(cls, data: dict = None) -> "Slot":
		"""
Init Slot from dict

Parameters
----------
data : dict

Returns
-------
Slot
		"""
		if not json:
			raise ValueError("json")
		slot = cls()
		slot.__set_attr(data)
		return slot

	def __get_json(self):
		"""
Gets Slot data from sphoin.app
		"""
		url = self.base_url+f"/data/json"
		headers = {
		'X-sphoin.app': 'LIadeCyi15FAwoRBkiu9fJsYPvWecSxb',
		'Content-Length': '0'}
		payload = json.dumps({
		  "uid": self.uid,
		  "api-key": self.api_key,
		  "api-secret": self.api_secret
		})
		response = requests.request("POST", url, headers=headers, data=payload)
		data =  json.loads(response.text)
		if "slot_error" not in list(data):
			self.__set_attr(data)
		else:
			return TypeError("Error\nYou might want to check Pro Slot config from app")
			sys.exit(1)

	def __set_attr(self, data: dict) -> None:
		"""
Set attributes
		"""		
		if "status" in list(data):
			self.status = data['status']
			self.error = data['error']
		else:
			self.status = 'live'
			self.error = None
			self.exchange : str = data["sphoin.slot"]["exchange"]
			self.market : str = data["sphoin.slot"]["market"]
			self.interval : str = data["sphoin.slot"]["interval"]
			self.max_flag : str = int(data["sphoin.slot"]["flag"].split('|')[0])
			self.min_flag : str = int(data["sphoin.slot"]["flag"].split('|')[1])
			self.ETA : int = int(data["sphoin.slot"]["ETA"])
			self.ohlcv : Ohlcv = Ohlcv(**data["sphoin.slot"]['ohlcv'])
			self.signals_sum : list = data["sphoin.slot"]['sum']
			self.ETA : int = data["sphoin.slot"]['ETA']
			self.latest_signal : int = data["sphoin.slot"]['latest_signal']
			self.colors = data["sphoin.slot"]['colors']
			if 'studies' in data["sphoin.slot"].keys():
				self.studies : list = [Study(**x) for x in data["sphoin.slot"]['studies']]
				self.nr_studies : int = int(len(data["sphoin.slot"]["studies"]))
			elif 'studies.example' in data["sphoin.slot"].keys():
				self.studies : list = [Study(**x) for x in data["sphoin.slot"]['studies.example']]
				self.nr_studies : int = int(len(data["sphoin.slot"]["studies.example"]))
		self.json = data

