#!/usr/bin/python3
import requests
import json

url = "http://api.weatherapi.com/v1/current.json"
params={"key":"c0aba767681e4adcaa0160828242809",
        "q":"London"}

response = requests.get(url, params=params)
data = response.json()
print(data)