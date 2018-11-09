import requests
import json
import re


class Search:
	"""Search a vine only in vivio"""
	def page_result(self, www, ob_find, page_number='1'):
		data = requests.get(www + ob_find + '&amp;start=' + page_number)
		result = data.text.split('\n')
		return result

	def convert(self, data):
		for res in data:
			if '"name":' in res:
				result = json.loads(res)
				return result

	def vine_id(self, url):
		data_request = requests.get(url)
		data = str(data_request.content)
		result = re.findall('https://www.vivino.com/.+/w/(\d+)', data)
		return result[0]

	def vine_comm(self, num):
		data = requests.get('https://www.vivino.com/api/wines/' + num + '/reviews?per_page=10')
		data = data.text
		return data

	def total(self, www, ob_find):
		names = []
		data_page = self.page_result(www, ob_find)
		data_json = self.convert(data_page)
		for data in data_json:
			dat = self.vine_id(data['@id'])
			result = [
				dict(id=dat, name=data['name'], image=data['image'])
			]
			names.append(result)
<<<<<<< HEAD
		return names
=======
		return result
>>>>>>> e85365fa5f6286e90fbeb5ded442aa4f78233461
