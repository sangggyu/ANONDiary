import sys, json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:thals@cluster0.kbk9mgh.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/diary')
def diary():
   return render_template('page_info.html')

@app.route("/diary/comment", methods=["GET"])
def diary_comment():
    return jsonify({'msg': '댓글 불러오기 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)