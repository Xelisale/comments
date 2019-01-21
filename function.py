import requests
import json
import re
import sqlite3
import logging


logging.basicConfig(filename='function.txt', level=logging.INFO)

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
		data = requests.get('https://www.vivino.com/api/wines/' + num + '/reviews?per_page=50')
		data = data.text
		return data

	def total(self, ob_find):
		""":return names: dict  a) vine id(unique number)
								b) vine name
								c) vine image(url)
		"""
		ob_find = ob_find.replace('"', "")
		names = []
		result1 = []

		def next_name(ob_find):
			""" change ob_find in list data """
			if ob_find == '':
				return result1
			result1.append(ob_find)

			def add_obj(obj):
				list_data = obj.split()
				separator = ' '
				obj = separator.join(list_data[:-1])
				return obj

			name = add_obj(ob_find)
			next_name(name)

		next_name(ob_find)

		for res in result1:
			logging.info(F"res : {res}")
			data_page = self.page_result(res)
			data_json = self.convert(data_page)
			if data_json:

				for data in data_json:
					dat = self.wine_id(data['@id'])
					result = [
						dict(id=dat, name=data['name'], image=data['image'])
					]
					names.append(result)

		return names

	def total2(self, ob_find):
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
		sql2 = """
			CREATE TABLE IF NOT EXISTS comments (
			numb INTEGER PRIMARY KEY AUTOINCREMENT, 
			wine_id INTEGER, 
			comment_text TEXT, 
			FOREIGN KEY(wine_id) REFERENCES data(id_wine))
		"""
		cursor.execute(sql)
		con.commit()
		cursor.execute(sql2)
		con.commit()
		con.close()

	def add_comment(self, comment, wine_id):
		con = sqlite3.connect(self.name_bd)
		cursor = con.cursor()
		sql = """
		INSERT INTO comments(wine_id, comment_text) VALUES (?,?)
		
		"""
		cursor.execute(sql, (wine_id, comment))
		con.commit()
		con.close()

	def check_id_comment(self, text):
		"""return data: new id or have id"""
		con = sqlite3.connect(self.name_bd)
		cursor = con.cursor()
		sql = """
			SELECT numb from comments where comment_text like ?
		"""
		cursor.execute(sql, (text,))
		data = cursor.fetchone()
		if data:
			return data
		con.close()

	def return_numb(self):
		con = sqlite3.connect(self.name_bd)
		cursor = con.cursor()
		sql = """
			SELECT numb FROM comments ORDER BY numb DESC LIMIT 1
		"""

		try:
			cursor.execute(sql)
			data = cursor.fetchone()

		except sqlite3.OperationalError:
			data = (1,)

		con.close()
		return data

	def check_id(self, id_wine):
		con = sqlite3.connect(self.name_bd)
		cursor = con.cursor()
		sql = "SELECT id_wine, data_request FROM data WHERE id_wine =" + id_wine
		cursor.execute(sql)
		data = cursor.fetchone()
		con.close()
		if data:
			return data[1]
		else:
			return []

	def select_all(self, id_wine):
		con = sqlite3.connect(self.name_bd)
		cursor = con.cursor()
		sql = "SELECT id_wine, data_request FROM data WHERE id_wine =" + id_wine
		cursor.execute(sql)
		data = cursor.fetchone()
		con.close()
		return data

	def insert(self, data_in):
		con = sqlite3.connect(self.name_bd)
		cursor = con.cursor()
		sql = """
					INSERT INTO data (id_wine, data_request, date_create) 
					VALUES (?,?, current_date)
				"""
		try:
			cursor.execute(sql, data_in)
			con.commit()
			con.close()
		except sqlite3.IntegrityError:
			print("This id is not unique")
			pass

	def update_bd(self, id_update):
		""":param id_update [id_wine, data]"""
		con = sqlite3.connect(self.name_bd)
		cursor = con.cursor()
		sql = """
			UPDATE data 
			SET data_request =?, date_create=CURRENT_DATE 
			WHERE id_wine=?
		 		"""
		try:
			cursor.execute(sql, (id_update[1], id_update[0]))
			con.commit()
			con.close()
		except sqlite3.IntegrityError:
			print("This id is not unique")
			pass
