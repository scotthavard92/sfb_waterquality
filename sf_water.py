import re
import requests
import json

#constants
url = 'https://infrastructure.sfwater.org/lims.asmx/getBeaches'
ifttt_url = 'https://maker.ifttt.com/trigger/advisory_detected/with/key/lGczdMXFN6c_U654HPO76S3U5T4Gqo50ZAsbaT3i1jG'
# station_url = 'https://infrastructure.sfwater.org/lims.asmx/getStation'

#functions
def grab_water_reports(url):
	r = requests.get(url)

	return r

def trim_response(response):
	result = re.search('>(.*)<', response)

	return result

def jsonify_reports(results):
	return json.loads(results)

def fetch_aquatic_park(data):
	for item in data:
		if item.get('stationid') == "4613":
			return item

	return None

def trigger_ifttt_webhook(item):
	if item["posted"] != None:
		print("alerting!")
		
		response = requests.post(ifttt_url)
		print(response.status_code)

#run
response = grab_water_reports(url)
res = trim_response(str(response.text))
data = jsonify_reports(res.group(1))
ap = fetch_aquatic_park(data)
trigger_ifttt_webhook(ap)
