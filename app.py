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
	base_page = search.page_result(SITE, request.json['name'])
	data = search.convert(base_page)
	t = 0
	for dat in data:
		url_page = search.vine_redirect_page(dat['@id'])
		# comments = search.vine_comments(url_page)
		result = {
			'id': t,
			'name': dat['name'],
			'image': dat['image'],
			'url': url_page[:-1],
			# 'done':  False
			# 'comments': comments,
		}
		names.append(result)
		t += 1
	with open('names.json', 'w') as file:
		json.dump(names, file)
		print('done')
	return jsonify({'names': names}), 201


@app.route('/comments/api/names/find/one/', methods=['POST'])
def one_comment():
	if not request.json or not 'id' in request.json:
		abort(400)
	with open('names.json', 'r') as file:
		dat = json.load(file)
	search = Search()
	print(request.json['id'])
	page = int(request.json['id'])
	page = dat[page]['url']
	comments = search.vine_comments(page)
	return jsonify({'page': comments}), 201


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
	app.run()
