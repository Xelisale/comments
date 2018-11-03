from flask import Flask, jsonify, abort
from flask import make_response, request
import json
from werkzeug.contrib.fixers import ProxyFix


from function import Search


app = Flask(__name__)

names = []
SITE = 'http://vivino.com/search/wines?q='

@app.route('/')
def base():
	return b'<b>Application in development</b>'


@app.route('/comments/api/names', methods=['GET'])
def get_all_name():
	with open('names.json', 'r') as file:
		names_all = json.load(file)
	return jsonify({'names': names_all})


@app.route('/comments/api/names/<int:names_id>', methods=['GET'])
def get_name(names_id):
	name = list(filter(lambda t: t['id'] == names_id, names))
	print(name)
	if len(name) == 0:
		abort(404)
	return jsonify({'name': name[0]})


@app.route('/comments/api/names/find/', methods=['POST'])
def names_find():
	if not request.json or not 'name' in request.json:
		abort(400)
	search = Search()
	base_page = search.page_result(SITE, request.json['name'])
	data = search.convert(base_page)
	t = 0
	for dat in data:
		result = {
			'id': t,
			'name': dat['name'],
			'image': dat['image'],
			# 'done':  False
		}
		names.append(result)
		t += 1
	with open('names.json', 'w') as file:
		json.dump(names, file)
		print('done')
	print(names)
	return jsonify({'names': names}), 201


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
	app.run()
