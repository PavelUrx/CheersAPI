from flask import Flask, request, jsonify
import json
from lphandler import *


app = Flask(__name__)




@app.route('/', methods=['GET', 'POST'])
def index():
    return 'hello world'

@app.route('/postdata', methods = ['POST', 'GET'])
def postdata():
    input_data = ''
    LpObject = LpObject()
    input_data = json.dumps(request.get_json())
    LpObject.solveForJson(input_data)
    return json.dumps(LpObject.getSolution())
