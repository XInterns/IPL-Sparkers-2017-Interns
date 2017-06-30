#!/usr/bin/python
from flask import Flask,json,Response, render_template
import getprediction
app = Flask(__name__, template_folder="webpage")


@app.route("/")
def home():
    return render_template('./home.html')
@app.route("/index.html")
def index1():
     return render_template('./index.html')




@app.route('/prediction/<int:mid>', methods=["GET"])
def api_article(mid):
    predictDictData = getprediction.getPrediction(mid) #return a dictionary data type {'name':"",prob: int_type}

    RESPONSE_JSON_DATA = json.dumps(predictDictData)
    RESPONSE = Response(RESPONSE_JSON_DATA, status=200, mimetype='application/json')
    return RESPONSE

if __name__ == '__main__':
    app.run(host="127.0.0.1",debug=True, port=int('3001'))
