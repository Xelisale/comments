from flask import Flask, jsonify, abort
from flask import make_response, request
import json
from werkzeug.contrib.fixers import ProxyFix


from function import Search


app = Flask(__name__)


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
	with open('names.json', 'r') as file:
		names = json.load(file)
	name = list(filter(lambda t: t['id'] == names_id, names))
	if len(name) == 0:
		abort(404)
	res = names[names_id]
	return jsonify({'name': res})


@app.route('/comments/api/names/find/', methods=['POST'])
def names_find():
	if not request.json or not 'name' in request.json:
		abort(400)
	search = Search()
	search.total(SITE, request.json['name'])
	with open('names.json', 'r') as file:
		names = json.load(file)
	return jsonify({'names': names}), 201


@app.route('/comments/api/names/find/one/', methods=['POST'])
def one_comment():
	comment = {}
	if not request.json or not 'id' in request.json:
		abort(400)
	search = Search()
	comments = search.vine_comm(request.json['id'])
	comments = json.loads(comments)
	result_all = comments['reviews']
	t = 0
	for result in result_all:
		comment[t] = result['note']
		t += 1
	return jsonify({'comment': comment}), 201


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
	app.run()
