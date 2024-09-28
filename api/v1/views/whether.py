#!/usr/bin/python3

import requests
import json

url = "http://api.weatherapi.com/v1/current.json"
params={"key":"c0aba767681e4adcaa0160828242809",
        "q":"London"}
def whether():
	response = requests.get(url, params=params)
	data = response.json()
	return data
# /api/v1/categories
# /api/v1/categories/events
# /api/v1/enroll
# /api/v1/myevents
# /api/v1/auth/reg
# /api/v1/auth/login
# /api/v1/auth/logout