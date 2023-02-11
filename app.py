import sys, json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

import certifi
ca = certifi.where()
# client = MongoClient('mongodb+srv://test:thals@cluster0.kbk9mgh.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
client = MongoClient('mongodb+srv://parkmj4312:Qkrp4918@cluster0.serijac.mongodb.net/?retryWrites=true&w=majority')

db = client.dbsparta

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/diary')
def diary():
  return render_template('page_info.html')
@app.route("/diary/save", methods=["POST"])
def diary_save():
    diary_list = list(db.anondiary.find({}))
    numlist = [0]
    for a in diary_list:
        numlist.append(a['num'])
    count = max(numlist) + 1
    name = request.form['name_give']
    comment = request.form['comment_give']
    doc = {
    'num':count,
    'name':name,
    'comment':comment
    }
    db.anondiary.insert_one(doc)
    return jsonify({'msg': '일기 기록 완료!'})
@app.route("/diary/show", methods=["GET"])
def diary_get():
    num = request.form['num_give']
    diary = db.anondiary.find_one({'num': num})
    return jsonify({'diary':diary})

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)