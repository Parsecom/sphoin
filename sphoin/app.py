"""Main module."""

__author__ = "pom11"
__copyright__ = "Copyright 2022, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "1.0.10"
__maintainer__ = "pom11"
__email__ = "office@parsecom.ro"

from sphoin.utils import get_terminal_size

import requests
import json
import time
import sys,select
import os
import datetime as dt

class Slot():

	def __init__(self,**kwargs):
		self.base_url = "https://api.sphoin.app/api/v1"
		if "config" in kwargs:
			self.config(file=kwargs["config"])
		else:
			if "api_key" not in kwargs:
				raise ValueError("api_key")
			elif "api_secret" not in kwargs:
				raise ValueError("api_secret")
			elif "uid" not in kwargs:
				raise ValueError("uid")
			self.api_key = kwargs["api_key"]
			self.api_secret = kwargs["api_secret"]
			self.uid = kwargs["uid"]
		
		#init size
		if "sizeX" in kwargs:
			self.sizeX = kwargs['sizeX']
		else:
			self.sizeX = None
		if "sizeY" in kwargs:
			self.sizeY = kwargs['sizeY']
		else:
			self.sizeY = None

	def config(self,file):
		while True:
			if file != "example":
				with open(file,"r") as f:
					data = json.load(f)
			else:
				data = {"uid" : "111YOURUID111","api-secret" : "111YOURSECRET111","api-key":"111YOURAPIKEY111","show" : ["line","studies","signals"]}
			self.api_key = data["api-key"]
			self.api_secret = data["api-secret"]
			self.uid = data["uid"]
			
			j = self.json()
			if "slot_error" not in list(j):
				if not isinstance(data["show"],list):
					raise ValueError("show not list")
				self.loop = data["show"]
				self.evaluate(banner=True)
			else:
				print("Error\nYou might want to check Pro Slot config")
				sys.exit()


	def evaluate(self,banner=True):
		while True:
			prt = []
			self.ctime = time.time()
			sizeX, sizeY = get_terminal_size()
			self.sizeX, self.sizeY = sizeX-1,sizeY-2
			screenX, screenY = self.sizeX, self.sizeY-1
			if len(self.loop)>1 and isinstance(self.loop,list):
				if "studies" in self.loop:
					studiesY = self.nr_studies
				else:
					studiesY = 0
				if "signals" in self.loop:
					sumY = self.nr_studies+self.nr_studies+1
				else:
					sumY = 0
				if "studies" in self.loop or "signals" in self.loop:
					screenY = screenY - studiesY - sumY
					ratio = divmod(screenY,(len(self.loop)-self.loop.count("studies")-self.loop.count("signals")))[0]
					rest = divmod(screenY,(len(self.loop)-self.loop.count("studies")-self.loop.count("signals")))[1]
				else:
					ratio = divmod(screenY,(len(self.loop)))[0]
					rest = divmod(screenY,(len(self.loop)))[1]
				for i,j in enumerate(self.loop):
					if j == "studies":
						self.sizeY = studiesY
						prt.append(getattr(self, j)())
					elif j == "signals":
						self.sizeY = sumY
						prt.append(getattr(self, j)())
					else:
						self.sizeY = ratio
						prt.append(getattr(self, j)())
					time.sleep(0.1)


			elif len(self.loop)==1 and isinstance(self.loop,list):	
				prt.append(getattr(self, self.loop[0])())
			elif not isinstance(self.loop,list):	
				prt.append("show not list")
			try:
				self.ETA = self.ETA - (time.time()-self.ctime) if self.ETA - (time.time()-self.ctime) >0 else 0
				os.system("clear")
				print("\n".join(prt))
				if banner:
					banner = self.banner()
					print(banner)
				self.await_key(10)
				if self.ETA == 0:
					break

			except Exception as e:
				print(str(e))
				print("\x1b[30;41;5merror\x1b[0m")
				time.sleep(1)


	def await_key(self,ETA):
		t, o, i = select.select([sys.stdin],[],[],ETA)
		if t:
			t = sys.stdin.readline().strip().split("|")
			self.on_key(t)
			

	def on_key(self,t):
		if t[0] in ["-h","--help","h"]:
			print("\tQuit - Q q")
			print("\tEnter - Refresh")
			time.sleep(10)
		elif t[0] in ["Q","q"]:
			os.system("clear")
			sys.exit()
		os.system("clear")


	def dot(self, time=True):
		url = self.base_url+f"/plot/dot/{self.sizeX}/{self.sizeY}"
		headers = {
		'X-sphoin.app': 'LIadeCyi15FAwoRBkiu9fJsYPvWecSxb',
		'Content-Length': '0'}
		payload = json.dumps({
		  "uid": self.uid,
		  "api-key": self.api_key,
		  "api-secret": self.api_secret
		})
		response = requests.request("POST", url, headers=headers, data=payload)
		response = response.text[:-5]
		if time == False:
			return(response[:response.find('\x1b[0m\n\x1b[30;43;2m········time\x1b[0m')])
		return(response)

	def line(self, time=True):
		url = self.base_url+f"/plot/line/{self.sizeX}/{self.sizeY}"
		headers = {
		'X-sphoin.app': 'LIadeCyi15FAwoRBkiu9fJsYPvWecSxb',
		'Content-Length': '0'}
		payload = json.dumps({
		  "uid": self.uid,
		  "api-key": self.api_key,
		  "api-secret": self.api_secret
		})
		response = requests.request("POST", url, headers=headers, data=payload)
		response = response.text[:-5]
		if time == False:
			return(response[:response.find('\x1b[0m\n\x1b[30;43;2m········time\x1b[0m')])
		return(response)

	def studies(self):
		url = self.base_url+f"/plot/studies/{self.sizeX}"
		headers = {
		'X-sphoin.app': 'LIadeCyi15FAwoRBkiu9fJsYPvWecSxb',
		'Content-Length': '0'}
		payload = json.dumps({
		  "uid": self.uid,
		  "api-key": self.api_key,
		  "api-secret": self.api_secret
		})
		response = requests.request("POST", url, headers=headers, data=payload)
		return(response.text[:-5])

	def signals(self):
		url = self.base_url+f"/plot/signals/{self.sizeX}/{self.sizeY}"
		headers = {
		'X-sphoin.app': 'LIadeCyi15FAwoRBkiu9fJsYPvWecSxb',
		'Content-Length': '0'}
		payload = json.dumps({
		  "uid": self.uid,
		  "api-key": self.api_key,
		  "api-secret": self.api_secret
		})
		response = requests.request("POST", url, headers=headers, data=payload)
		return(response.text[:-8])

	def banner(self):
		emp = dt.timedelta(seconds=int(self.ETA))
		disp1 = f"{self.exchange} \x1b[30;47;5m| {self.market} | {self.interval} \x1b[30;43;5m"
		disp2 = f"| Threshold \x1b[30;47;5m| {self.buy_threshold} | {self.sell_threshold} \x1b[30;43;5m"
		disp3 = f"| ETA \x1b[30;47;5m| {emp} \x1b[30;43;5m"
		disp0 = "Enter refresh | h help | q Quit"
		disp1 = f"{disp1}{disp2}{disp3}".ljust(int(self.sizeX/2*1.6)," ")
		disp0 = disp0.rjust(int(self.sizeX/2*0.4)," ")
		banner = disp1+disp0
		banner = banner.ljust(self.sizeX+1," ")
		return "\x1b[30;43;5m"+banner+"\x1b[0m"

	def json(self):
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
			self.exchange = data["sphoin.slot"]["exchange"]
			self.market = data["sphoin.slot"]["market"]
			self.interval = data["sphoin.slot"]["interval"]
			self.buy_threshold = int(data["sphoin.slot"]["flag"].split('|')[0])
			self.sell_threshold = int(data["sphoin.slot"]["flag"].split('|')[1])
			self.ETA = int(data["sphoin.slot"]["ETA"])
			try:	
				self.nr_studies = int(len(list(data["sphoin.slot"]["studies"])))
			except:
				self.nr_studies = int(len(list(data["sphoin.slot"]["studies.example"])))
		return data