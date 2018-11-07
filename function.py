import requests
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By


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

	def vine_redirect_page(self, url):
		data2 = requests.get(url)
		data = str(data2.content)
		result = re.findall('https://www.vivino.com/.+/w/\d+', data)
		result = result[0].split("'")
		return result[0]

	def vine_comments(self, page):
		result = []
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		options.add_argument(
			'--user-agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"')
		options.add_argument('--no-sandbox')
		options.add_argument("--disable-dev-shm-usage")
		driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver' ,chrome_options=options)
		driver.get(page)
		name_element = driver.find_elements_by_class_name('communityReview__textSection--vu-i-')
		for res in name_element:
			result.append(res.text)
		return result
