"""Main module."""

__author__ = "pom11"
__copyright__ = "Copyright 2023, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "2.0.5"
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

Parameters
----------
config : str
	Absolute path of yaml configuration file
	Example:
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
	"""
	def __init__(self,**kwargs) -> None:
		self.show_banner : bool = False
		self.base_url : str = "https://api.sphoin.app/api/v1"
		if "config" in kwargs:
			self.__from_file(file=kwargs["config"])
		else:
			self.__from_kwargs(kwargs)

	def refresh(self):
		"""
Updates Slot values with new data
		"""
		self.__get_json()

	def __get_screenSize(self,data={}):
		if "sizeX" in data.keys():
			self.sizeX : int = data['sizeX']
		else:
			self.sizeX : int = None
		if "sizeY" in data.keys():
			self.sizeY : int = data['sizeY']
		else:
			self.sizeY : int = None

	def __from_file(self,file):
		"""
Reads yaml config file
		"""
		if file != "example":
			with open(file,"r") as f:
				self.config = file
				data = yaml.safe_load(f)
		else:
			self.config = None
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
		self.api_key : str = data["api-key"]
		self.api_secret : str = data["api-secret"]
		self.uid : str = data["uid"]
			
		try:
			if not isinstance(data["layout"],list):
				raise ValueError("layout not list")
			elif not any([x in data["layout"] for x in ['line','studies','signals','time','footer']]):
				raise ValueError("layout expected values: line, studies, signals, time, footer")
			else:
				self.layout : list = data["layout"]
		except Exception as e:
			self.layout = [
					"line",
					"time",
					"studies",
					"signals",
					"footer"
					]

		self.__get_screenSize(data)
		self.__get_json()
		
	def __from_kwargs(self,kwargs):
		"""
Init Slot from arguments
		"""
		self.config = None
		if "api_key" not in kwargs:
			raise ValueError("api_key")
		elif "api_secret" not in kwargs:
			raise ValueError("api_secret")
		elif "uid" not in kwargs:
			raise ValueError("uid")
		self.api_key : str = kwargs["api_key"]
		self.api_secret : str = kwargs["api_secret"]
		self.uid : str = kwargs["uid"]
		try:
			if 'layout' is kwargs.keys():
				if not isinstance(kwargs["layout"],list):
					raise ValueError("layout not list")
				elif not any([x in kwargs["layout"] for x in ['line','studies','signals','time','footer']]):
					raise ValueError("layout list expected values: line, studies, signals, time, footer")
				else:
					self.layout : list = kwargs["layout"]
			else:
				raise ValueError("layout list missing")
		except Exception as e:
			self.layout = [
					"line",
					"time",
					"studies",
					"signals",
					"footer"
					]

		self.__get_screenSize(kwargs)
		self.__get_json()

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
		else:
			return TypeError("Error\nYou might want to check Pro Slot config from app")
			sys.exit()
