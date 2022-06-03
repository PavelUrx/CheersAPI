from flask import Flask, request, jsonify
import json
from lphandler import *


app = Flask(__name__)
sess = Session()
app.config.from_object(__name__)
Session(app)
LpObject = LpObject()
input_data = ''

@app.route('/', methods=['GET', 'POST'])
def index():
    return 'hello world'

@app.route('/postdata', methods = ['POST', 'GET'])
def postdata():
    input_data = json.dumps(request.get_json())
    LpObject.solveForJson(input_data)
    return json.dumps(LpObject.getSolution())



if __name__ == '__main__':
    app.secret_key = 'AMkhPWeCFcHT57zf%$j^t&x^ENj8W6Bi'

    sess.init_app(app)

    app.debug = True
    app.run(port = 80, debug = False)