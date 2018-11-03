import requests
import json
import re


class Search:
	"""Search a vine only in vivio"""

	def page_result(self, www, ob_find):
		data = requests.get(www + ob_find)
		result = str(data.content).split('\\n')
		return result

	def convert(self, data):
		for res in data:
			if '"name":' in res:
				string_base = re.sub(r'\\x..', 'e', res)
				string_one = re.sub(r"\\'s", '', string_base)
				result = json.loads(string_one)
				# print(result)
				return result
			
	def vine_comments(self, page):
		for res in data:
			print(res)
