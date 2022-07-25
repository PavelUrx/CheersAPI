from flask import Flask, request, jsonify
import json
from lphandler import *


app = Flask(__name__)

input_data = ''
LpObject = LpObject()


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'hello world'

#obdrzi soubor json a vraci optimalni reseni
@app.route('/postdata', methods = ['POST', 'GET'])
def postdata():
    input_data = json.dumps(request.get_json())
    LpObject.solveForJson(input_data)
    return jsonify(LpObject.getSolution())

#if __name__ == "__main__":
 #   app.run()