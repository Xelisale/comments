import requests
import json
import re
import sqlite3


class Search:
	"""Search a vine only in vivio"""
	def __init__(self):
		self.site = 'http://vivino.com/search/wines?q='

	def page_result(self, ob_find):
		""":return result: all page"""
		data = requests.get(self.site + ob_find)
		result = data.text.split('\n')
		return result

	@staticmethod
	def convert(data):
		""" :param data: Page after search
			:return result: All coincidences
		"""
		for res in data:
			if '"name":' in res:
				result = json.loads(res)
				return result

	@staticmethod
	def wine_id(url):
		data_request = requests.get(url)
		data = str(data_request.content)
		result = re.findall('https://www.vivino.com/.+/w/(\d+)', data)
		return result[0]

	@staticmethod
	def wine_comm(num):
		data = requests.get('https://www.vivino.com/api/wines/' + num + '/reviews?per_page=10')
		data = data.text
		return data

	def total(self, ob_find):
		""":return names: dict  a) vine id(unique number)
								b) vine name
								c) vine image(url)
		"""
		names = []

		data_page = self.page_result(ob_find)
		data_json = self.convert(data_page)
		if data_json:

			for data in data_json:
				print(data)
				dat = self.wine_id(data['@id'])
				result = [
					dict(id=dat, name=data['name'], image=data['image'])
				]
				names.append(result)
			return names


class WorksDB:
	"""class to work on DB"""

	def __init__(self):
		self.name_bd = 'Databases.sqlite'

	def create_database(self):
		con = sqlite3.connect(self.name_bd)
		cursor = con.cursor()
		sql = """
			CREATE TABLE IF NOT EXISTS data (
				numb INTEGER PRIMARY KEY AUTOINCREMENT, 
				id_wine INTEGER unique, 
				data_request TEXT, 
				date_create TEXT
				);
		"""
		cursor.execute(sql)
		con.commit()
		con.close()

	def check_id(self, id_wine):
		con = sqlite3.connect(self.name_bd)
		cursor = con.cursor()
		sql = "SELECT id_wine, data_request FROM data WHERE id_wine =" + id_wine
		cursor.execute(sql)
		data = cursor.fetchone()
		if data:
			return data[1]
		else:
			return []

	def insert(self, data_in):
		con = sqlite3.connect(self.name_bd)
		cursor = con.cursor()
		sql = """
					INSERT INTO data (id_wine, data_request, date_create) VALUES (?,?, current_date)
				"""
		try:
			cursor.execute(sql, data_in)
			con.commit()
			con.close()
		except sqlite3.IntegrityError:
			print("This id is not unique")
			pass

	def update_bd(self, id_update):
		""":param id_in [id_wine, data]"""
		con = sqlite3.connect(self.name_bd)
		cursor = con.cursor()
		sql = "UPDATE data SET data.data_request =" + id_update[1] + \
		      ", data.date_create=current_date WHERE data.id_wine=" + id_update[0]
		try:
			cursor.execute(sql)
			con.commit()
			con.close()
		except sqlite3.IntegrityError:
			print("This id is not unique")
			pass
