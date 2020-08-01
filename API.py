from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from json import loads
import os

from amazonsearch import search

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"*": {"origins": os.environ.get('WEB')}})

@app.route('/')
def root():
  params = loads(request.args.get('params', default = '', type = str))
  return jsonify({ 'a': params['search'], 'b': 2 })

@app.route('/amazonsearch')
def amazonsearch():
  params = loads(request.args.get('params', default = '', type = str))
  search_term = params['search']
  result = search(search_term)

  return jsonify(result)