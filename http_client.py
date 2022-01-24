import requests

def make_request(url):
    res = requests.get(url)
    return res.json()