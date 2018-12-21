from flask import Flask, jsonify, abort
from flask import make_response, request
import json
from werkzeug.contrib.fixers import ProxyFix

from function import Search, WorksDB

app = Flask(__name__)


@app.route('/api/names', methods=['GET'])
def get_all_name():
	with open('names.json', 'r') as file:
		names_all = json.load(file)

	return jsonify({'names': names_all})


@app.route('/api/names/find/', methods=['POST'])
def names_find():
	"""	Find and return all match in POST request.
		Name in POST request necessary parameter
	"""
	if not (request.json and 'name' in request.json):
		abort(400)

	search = Search()
	names = search.total(request.json['name'])

	if names:
		return jsonify({'names': names}), 201

	else:
		abort(404)


@app.route('/api/names/find/id/', methods=['POST'])
def one_comment():
	""" :param requst.json: id number vine
		:return comment:   information user and comments
	"""
	result = []

	if not (request.json and 'id' in request.json):
		abort(400)

	search = Search()
	work_bd = WorksDB()
	work_bd.create_database()
	data = work_bd.check_id(request.json['id'])

	if not ('cache' in request.json) and len(data) != 0:
		return jsonify({'comments': data}), 201

	else:
		comments = json.loads(search.wine_comm(request.json['id']))
		result_all = comments['reviews']

		for result_one in result_all:
			comment = {
				(result_one['user']['alias']):
					{
						'image': result_one['user']['image'],
						'note': result_one['note']
					}
			}
			result.append(comment)
		bd_data = [request.json['id'], str(result)]

		if not 'cache' in request.json:
			work_bd.insert(bd_data)

		else:
			work_bd.update_bd(bd_data)

	return jsonify({'comment': result}), 201


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
	app.run()
