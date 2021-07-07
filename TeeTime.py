from typing import Union, List
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import configparser
import requests
import json


		
class TeeTime:
	def __init__(self):
		configParser = configparser.RawConfigParser()  
		configParser.read(r'.\config.txt')
		
		self.teeTimeLockerString = ""
		self.base_url = "https://www.tee-on.com/PubGolf/servlet/"
		self.session = requests.Session()
		self.courseSelected = False
		
		for configs in configParser.sections():
			for (each_key, each_val) in configParser.items(configs):
				if each_key == "date": self.teeTimeDate = each_val
				if each_key == "time": self.teeTimeTime = each_val
				if each_key == "holes": self.teeTimeHoles = each_val
				if each_key == "players": self.teeTimePlayers = each_val
				if each_key == "carts": self.teeTimeCarts = each_val
				if each_key == "username": self.teeTimeUsername = each_val
				if each_key == "password": self.teeTimePassword = each_val
				if each_key == "preferred courses": self.teeTimeCourses = each_val.split(',')
		

		self.teeTimeUrls = {
			"loginURL": "com.teeon.teesheet.servlets.ajax.CheckSignInAjax",
			"loginHome": "com.teeon.teesheet.servlets.golfersection.GolferSectionHome",
			"beginBookTeeTimes": "com.teeon.teesheet.servlets.golfersection.WebBookingSearchSteps",
			"bookTeeTimes": "com.teeon.teesheet.servlets.golfersection.WebBookingSearchResults",
			"bookMoreTeeTimes": "com.teeon.teesheet.servlets.golfersection.WebBookingMoreTimes",
			"checkBookingLock": "com.teeon.teesheet.servlets.golfersection.CheckBookingLock",
			"bookingChooseCarts": "com.teeon.teesheet.servlets.golfersection.WebBookingChooseCarts",
			"bookingPlayerEntry": "com.teeon.teesheet.servlets.golfersection.WebBookingPlayerEntry",
			"bookingBookTime": "com.teeon.teesheet.servlets.golfersection.WebBookingBookTime"
		}



		
	def formatHTML(self, res):
		soup = BeautifulSoup(res.content, "lxml")
		return soup
		
	def getLockerString(self, soup):
		return soup.find("input", {"name":"LockerString"})['value']
		
	def getTeeTimes(self, soup):
		return_times = []
		prices = soup.findAll("p", {"class": "price"})
		times = soup.findAll("p", {"class":"time"})
		for time, price in zip(times, prices):
			if len(price.text) == 0:
				return_times.append(time)
				
		return return_times if return_times else []
		
	def get(self, endpoint: str, func: str, data: dict = {}) -> Union[requests.Response, None]:
		if func == "bookTeeTimes_func":
			params = {
				"CourseCode": "",
				"BackTarget": "com.teeon.teesheet.servlets.golfersection.GolferSectionHome",
				"Referrer": "www.tee-on.com"
			}
			res = self.formatHTML(self.session.get(url=self.base_url+endpoint, data=params))
			return res
		elif func == "checkBook_func":
			res = self.formatHTML(self.session.get(url=self.base_url+endpoint, data=data))
			return res
		
		return
		

		
	def post(self, endpoint: str, func: str, data: dict = {},  ) -> Union[requests.Response, None]:
		if func == "login_func":
			data_login = {
				"Username": self.teeTimeUsername,
				"Password": self.teeTimePassword,
				"FromTeeOn": "true",
				"Target": "com.teeon.teesheet.servlets.golfersection.GolferSectionHome",
				"FailTarget": "/login_failed.html"
			}
			res = self.formatHTML(self.session.post(url=self.base_url+endpoint, data=data_login))
			if res:
				return res
			return None
		elif func == "course_func":
			res = self.formatHTML(self.session.post(url=self.base_url+endpoint, params=data))
			if res:
				return res
			return None
		elif func == "chooseCarts_func":
			res = self.formatHTML(self.session.post(url=self.base_url+endpoint, params=data))
			if res:
				return res
			return None
		elif func == "bookCart_func":
			res = self.formatHTML(self.session.post(url=self.base_url+endpoint, params=data))
			return res
		elif func == "bookTime_func":
			res = self.formatHTML(self.session.post(url=self.base_url+endpoint, params=data))
			return res
			

