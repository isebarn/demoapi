from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from json import loads
import os

import amazonsearch as amazon
import zillowsearch as zillow

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"*": {"origins": os.environ.get('WEB')}})

@app.route('/')
def root():
  return jsonify({ 'a': 1, 'b': 2 })

@app.route('/amazonsearch')
def amazonsearch():
  params = loads(request.args.get('params', default = '', type = str))
  search_term = params['search']
  result = amazon.search(search_term)

  return jsonify(result)

@app.route('/zillow_zip_search')
def zillow_zip_search():
  params = loads(request.args.get('params', default = '', type = str))
  search_term = params['search']
  result = zillow.zip_search(search_term)
  print(result)

  return jsonify(result)