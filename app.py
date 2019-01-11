import json
from flask import Flask, jsonify, abort
from flask import make_response, request
from werkzeug.contrib.fixers import ProxyFix


from function import Search, WorksDB

app = Flask(__name__)


@app.route('/api/names', methods=['GET'])
def get_all_name():
	with open('names.json', 'r') as file:
		names_all = json.load(file)

	return jsonify({'names': names_all})

@app.route('/api/comments/<int:id>', methods=['GET'])
def id_comments(id):
	""" :param requst.json['id']: id number vine
		:return comment:   information user and comments
	"""
	id = str(id)
	result = []
	search = Search()
	work_bd = WorksDB()
	work_bd.create_database()

	comments = json.loads(search.wine_comm(id))
	result_all = comments['reviews']

	for result_one in result_all:
		id_comments = work_bd.check_id_comment(result_one['note'])

		if id_comments:
			id_comments = id_comments[0]

		else:
			work_bd.add_comment(result_one['note'], id)
			id_comments = work_bd.return_numb()
			id_comments = int(id_comments[0]) + 1

		comment = {
			'author': result_one['user']['alias'],
			'image': result_one['user']['image'],
			'note': {'id': id_comments,
					 'text': result_one['note']}
		}

		result.append(comment)

	bd_data = [id, str(result)]
	work_bd.insert(bd_data)

	return jsonify({'comment': result}), 201


@app.route('/api/comments1/', methods=['GET'])
def all_list():
	work_bd = WorksDB()
	result = work_bd.select_all('1582466')
	result = result[1]
	return jsonify({'comment': result}), 201


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
	""" :param requst.json['id']: id number vine
		:return comment:   information user and comments
	"""
	result = []

	if not (request.json and 'id' in request.json):
		abort(400)

	search = Search()
	work_bd = WorksDB()
	work_bd.create_database()
	id = request.json['id']
	data = work_bd.check_id(id)

	if not ('cache' in request.json) and len(data) != 0:
		return jsonify({'comments': data}), 201

	else:
		comments = json.loads(search.wine_comm(id))
		result_all = comments['reviews']

		for result_one in result_all:
			id_comments = work_bd.check_id_comment(result_one['note'])

			if id_comments:
				id_comments = id_comments[0]
			else:
				work_bd.add_comment(result_one['note'], id)
				id_comments = work_bd.return_numb()
				id_comments = int(id_comments[0]) + 1

			comment = {
				'author': result_one['user']['alias'],
				'image': result_one['user']['image'],
				'note': {'id': id_comments,
						'text': result_one['note']}
			}

			result.append(comment)

		bd_data = [id, str(result)]

		if 'cache' in request.json:
			work_bd.update_bd(bd_data)

		else:
			work_bd.insert(bd_data)

	return jsonify({'comment': result}), 201


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
	app.run()
