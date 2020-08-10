from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS, cross_origin
from json import loads
import os

import amazonsearch as amazon
import zillowsearch as zillow
import DisonORM as dison
import rightmove as right
import turkey
from time import sleep

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

  return jsonify(result)

@app.route('/dison_books')
def dison_books():
  result = dison.Operations.GetBooks()

  return jsonify(result)

@app.route('/dison_ebookcategories')
def dison_ebookcategories():
  result = dison.Operations.GetEBookCategories()

  return jsonify(result)

@app.route('/excelfile')
def excelfile():
  os.remove("/home/david/Downloads/file.xlsx")

  #params = loads(request.args.get('params', default = '', type = str))
  #start = params['start']
  #end = params['end']
  #turkey.get_data(start, end)
  return send_from_directory('/home/david/Downloads' ,'data.xlsx', as_attachment=True)
  #return send_from_directory('/home/selenium_chrome_downloads/' ,'FonTurkey_Fon_Karsilastirma.xlsx', as_attachment=True)

@app.route('/rightmove')
def rightmove():
  params = loads(request.args.get('params', default = '', type = str))
  search_term = params['search']
  print(search_term)
  result = right.search(search_term)
  return jsonify(result)

@app.route('/generate_excel')
def generate_excel():
  try:
    os.remove("/home/selenium_chrome_downloads/FonTurkey_Fon_Karsilastirma.xlsx")

  except Exception as e:
    pass

  try:
    params = loads(request.args.get('params', default = '', type = str))
    start = params['start']
    end = params['end']
    turkey.get_data(start, end)

  except Exception as e:
    pass

  return '1'


@app.route('/get_excel')
def get_excel():
  return send_from_directory('/home/selenium_chrome_downloads/' ,'FonTurkey_Fon_Karsilastirma.xlsx', as_attachment=True)
