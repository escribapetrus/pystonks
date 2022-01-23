import json

def get_contents(filename):
    with open(filename) as f:
        lines = f.readlines()
    return json.loads(lines[0])