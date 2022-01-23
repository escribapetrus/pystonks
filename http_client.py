import requests
import json
import os

def make_request(url):
    res = requests.get(url)
    return res.json()