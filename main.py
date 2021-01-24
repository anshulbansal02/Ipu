import percy
import json
import requests

data = percy.parse('./data/result1.pdf')


with open('./data/result_parsed.json', 'w') as result_file:
    result_file.write(json.dumps(data))